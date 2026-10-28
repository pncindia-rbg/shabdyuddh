"""SQLite storage: finished matches and per-player leaderboard totals."""
import sqlite3

SCHEMA = """
CREATE TABLE IF NOT EXISTS matches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lang TEXT NOT NULL,
    played_at TEXT DEFAULT CURRENT_TIMESTAMP,
    p1 INTEGER NOT NULL,
    p2 INTEGER NOT NULL,
    s1 INTEGER NOT NULL,
    s2 INTEGER NOT NULL,
    winner INTEGER
);
CREATE TABLE IF NOT EXISTS players (
    tg_id INTEGER PRIMARY KEY,
    name TEXT,
    matches INTEGER DEFAULT 0,
    wins INTEGER DEFAULT 0,
    points INTEGER DEFAULT 0
);
-- Referral tree: one row per user, upline fixed at first capture (first /start wins).
CREATE TABLE IF NOT EXISTS referrals (
    tg_id INTEGER PRIMARY KEY,
    name TEXT,
    level1 INTEGER,
    level2 INTEGER,
    level3 INTEGER,
    joined_at TEXT DEFAULT CURRENT_TIMESTAMP
);
-- Entry fees charged (stub for now). fee_micro = fee in millionths of a Pi.
CREATE TABLE IF NOT EXISTS entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    payer INTEGER NOT NULL,
    fee_micro INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'charged',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
-- Per-user UI language picked via /start buttons (hi, en, vi, id, ar).
CREATE TABLE IF NOT EXISTS user_lang (
    tg_id INTEGER PRIMARY KEY,
    lang TEXT NOT NULL,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);
-- Commission ledger. amount_micro in millionths of a Pi. pct_bp in basis points (500 = 5%).
CREATE TABLE IF NOT EXISTS commissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entry_id INTEGER NOT NULL,
    payer INTEGER NOT NULL,
    beneficiary INTEGER NOT NULL,
    level INTEGER NOT NULL,
    pct_bp INTEGER NOT NULL,
    amount_micro INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',
    note TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
"""

# level -> (referrals column, commission in basis points of the entry fee)
LEVELS = [(1, "level1", 500), (2, "level2", 300), (3, "level3", 200)]
PENDING_NOTE = "pending until payment live"


def connect(path):
    conn = sqlite3.connect(path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    return conn


def record_match(conn, lang, players, totals, winner_uid):
    """players: [(uid, name), (uid, name)]; totals: [pts1, pts2]; winner_uid None means draw."""
    cur = conn.execute(
        "INSERT INTO matches (lang, p1, p2, s1, s2, winner) VALUES (?, ?, ?, ?, ?, ?)",
        (lang, players[0][0], players[1][0], totals[0], totals[1], winner_uid),
    )
    for (uid, name), pts in zip(players, totals):
        win = 1 if uid == winner_uid else 0
        conn.execute(
            """INSERT INTO players (tg_id, name, matches, wins, points) VALUES (?, ?, 1, ?, ?)
               ON CONFLICT(tg_id) DO UPDATE SET
                 name = excluded.name,
                 matches = matches + 1,
                 wins = wins + excluded.wins,
                 points = points + excluded.points""",
            (uid, name, win, pts),
        )
    conn.commit()
    return cur.lastrowid


def leaderboard(conn, limit=10):
    return conn.execute(
        "SELECT name, matches, wins, points FROM players ORDER BY wins DESC, points DESC LIMIT ?",
        (limit,),
    ).fetchall()


def capture_referral(conn, uid, name, ref_uid=None):
    """Create the referral row for a new user. Upline is fixed at first capture (first /start wins).

    Returns one of: 'new_with_ref', 'new_no_ref', 'exists', 'self', 'bad_ref'.
    """
    row = conn.execute("SELECT 1 FROM referrals WHERE tg_id = ?", (uid,)).fetchone()
    if row:
        conn.execute("UPDATE referrals SET name = ? WHERE tg_id = ?", (name, uid))
        conn.commit()
        return "exists"
    if ref_uid is None:
        conn.execute("INSERT INTO referrals (tg_id, name) VALUES (?, ?)", (uid, name))
        conn.commit()
        return "new_no_ref"
    if ref_uid == uid:
        conn.execute("INSERT INTO referrals (tg_id, name) VALUES (?, ?)", (uid, name))
        conn.commit()
        return "self"
    up = conn.execute(
        "SELECT tg_id, level1, level2 FROM referrals WHERE tg_id = ?", (ref_uid,)
    ).fetchone()
    if up is None:
        # referrer never started the bot, so there is no chain to attach to
        conn.execute("INSERT INTO referrals (tg_id, name) VALUES (?, ?)", (uid, name))
        conn.commit()
        return "bad_ref"
    # uid's upline: level1 = referrer, level2 = referrer's level1, level3 = referrer's level2.
    # Uplines always point to users created earlier, so the tree cannot loop.
    conn.execute(
        "INSERT INTO referrals (tg_id, name, level1, level2, level3) VALUES (?, ?, ?, ?, ?)",
        (uid, name, up["tg_id"], up["level1"], up["level2"]),
    )
    conn.commit()
    return "new_with_ref"


def record_entry(conn, payer_uid, fee_pi):
    """Log an entry fee and write one pending commission row per upline level that exists.

    Returns (entry_id, [commission rows as dicts]).
    """
    fee_micro = round(fee_pi * 1_000_000)
    cur = conn.execute("INSERT INTO entries (payer, fee_micro) VALUES (?, ?)", (payer_uid, fee_micro))
    entry_id = cur.lastrowid
    row = conn.execute("SELECT level1, level2, level3 FROM referrals WHERE tg_id = ?", (payer_uid,)).fetchone()
    made = []
    if row:
        for level, col, bp in LEVELS:
            ben = row[col]
            if not ben:
                continue
            amt = fee_micro * bp // 10000
            conn.execute(
                """INSERT INTO commissions (entry_id, payer, beneficiary, level, pct_bp, amount_micro, status, note)
                   VALUES (?, ?, ?, ?, ?, ?, 'pending', ?)""",
                (entry_id, payer_uid, ben, level, bp, amt, PENDING_NOTE),
            )
            made.append({"beneficiary": ben, "level": level, "pct_bp": bp, "amount_micro": amt})
    conn.commit()
    return entry_id, made


def void_entry(conn, entry_id):
    """Entry refunded before pairing: its pending commissions are voided."""
    conn.execute("UPDATE entries SET status = 'refunded' WHERE id = ?", (entry_id,))
    conn.execute(
        "UPDATE commissions SET status = 'void', note = 'entry refunded' WHERE entry_id = ? AND status = 'pending'",
        (entry_id,),
    )
    conn.commit()


def referral_summary(conn, uid):
    """Network counts per level and earned-so-far (pending) totals per level, in micro-Pi."""
    counts = {}
    for level, col, _ in LEVELS:
        counts[level] = conn.execute(
            f"SELECT COUNT(*) FROM referrals WHERE {col} = ?", (uid,)
        ).fetchone()[0]
    earned = {level: 0 for level, _, _ in LEVELS}
    for r in conn.execute(
        "SELECT level, SUM(amount_micro) AS s FROM commissions WHERE beneficiary = ? AND status = 'pending' GROUP BY level",
        (uid,),
    ).fetchall():
        earned[r["level"]] = r["s"] or 0
    return counts, earned



def get_lang(conn, uid):
    """Saved UI/match language for a user, or None if they never picked one."""
    row = conn.execute("SELECT lang FROM user_lang WHERE tg_id = ?", (uid,)).fetchone()
    return row["lang"] if row else None


def set_lang(conn, uid, lang):
    conn.execute(
        """INSERT INTO user_lang (tg_id, lang) VALUES (?, ?)
           ON CONFLICT(tg_id) DO UPDATE SET lang = excluded.lang, updated_at = CURRENT_TIMESTAMP""",
        (uid, lang),
    )
    conn.commit()
