"""Shabd Yuddh Pi Mini App backend. Reuses game.py and db.py from the bot folder."""
import hashlib
import os
import secrets
import sys
import threading
import time
from pathlib import Path

import httpx
from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

BOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BOT_DIR))
import db  # noqa: E402
import game  # noqa: E402

HERE = Path(__file__).resolve().parent

# ---- settings (env only; nothing here holds secrets) ----
PI_APP_ID = os.environ.get("PI_APP_ID", "").strip()
PI_APP_SECRET = os.environ.get("PI_APP_SECRET", "").strip()
PI_ENV = os.environ.get("PI_ENV", "").strip().lower()          # sandbox | testnet
PI_API_BASE = os.environ.get("PI_API_BASE", "https://api.minepi.com/v2").rstrip("/")
PAYMENTS_ENABLED = bool(PI_APP_ID and PI_APP_SECRET and PI_ENV in ("sandbox", "testnet"))
SANDBOX = PI_ENV != "testnet"  # sandbox flag for the Pi SDK init on the frontend
ENTRY_FEE_PI = float(os.environ.get("ENTRY_FEE_PI", "0.5"))
ENTRY_MEMO = "Shabd Yuddh entry"
ROUND_SECONDS = int(os.environ.get("ROUND_SECONDS", "60"))
ROUNDS = int(os.environ.get("ROUNDS", "5"))
DB_PATH = os.environ.get("DB_PATH", str(BOT_DIR / "shabdyuddh.db"))
LANGS = ["en", "hi", "vi", "id", "ar"]
WORD_FILES = {l: str(BOT_DIR / "words" / f"{l}.txt") for l in LANGS}
WORDS = {l: game.load_words(p, l) for l, p in WORD_FILES.items() if Path(p).exists()}
VALID = {l: set(w) for l, w in WORDS.items()}

app = FastAPI(title="Shabd Yuddh Pi")
LOCK = threading.Lock()
CONN = db.connect(DB_PATH)
CONN.executescript("""
CREATE TABLE IF NOT EXISTS pi_users (
    internal_id INTEGER PRIMARY KEY,
    pi_uid TEXT UNIQUE NOT NULL,
    username TEXT
);
CREATE TABLE IF NOT EXISTS pi_payments (
    payment_id TEXT PRIMARY KEY,
    pi_uid TEXT NOT NULL,
    amount REAL,
    status TEXT NOT NULL,
    txid TEXT,
    used INTEGER DEFAULT 0,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
""")

SESSIONS = {}      # session token -> internal id
QUEUE = {l: [] for l in LANGS}   # lang -> [internal ids waiting]
MATCHES = {}       # match id -> Match
USER_MATCH = {}    # internal id -> match id
NAMES = {}         # internal id -> display name
_mid = [1]


def internal_id(pi_uid: str) -> int:
    # Telegram ids are small, so Pi ids live in a separate high range.
    return 10**15 + int(hashlib.sha256(pi_uid.encode()).hexdigest()[:12], 16)


class Match:
    def __init__(self, lang, a, b):
        self.id = _mid[0]
        _mid[0] += 1
        self.lang = lang
        self.players = [a, b]
        self.totals = {a: 0, b: 0}
        self.round_no = 0
        self.letters = []
        self.seed_counter = None
        self.best = {}
        self.active = False
        self.ends = 0.0
        self.next_at = time.time() + 2
        self.history = []
        self.finished = False
        self.winner = None

    def other(self, uid):
        return self.players[1] if self.players[0] == uid else self.players[0]


def _tick(m: Match):
    """Advance a match by wall clock: end an expired round, or start the next one when due."""
    if m.finished:
        return
    now = time.time()
    if m.active and now >= m.ends:
        _end_round(m, now)
    elif not m.active and m.round_no < ROUNDS and now >= m.next_at:
        _start_round(m, now)


def _start_round(m: Match, now):
    picked = game.pick_round(WORDS[m.lang])
    if picked is None:
        m.finished = True
        m.winner = "void"
        return False
    m.round_no += 1
    _, m.letters, m.seed_counter = picked
    m.best = {}
    m.active = True
    m.ends = now + ROUND_SECONDS
    return True


def _end_round(m: Match, now):
    m.active = False
    pts, words = {}, {}
    for uid in m.players:
        best = m.best.get(uid)
        pts[uid] = best[1] if best else 0
        words[uid] = best[0] if best else None
        m.totals[uid] += pts[uid]
    m.history.append({"n": m.round_no, "words": words, "pts": pts})
    if m.round_no >= ROUNDS:
        _finish(m)
    else:
        m.next_at = now + 4


def _finish(m: Match):
    a, b = m.players
    ta, tb = m.totals[a], m.totals[b]
    winner = a if ta > tb else b if tb > ta else None
    m.winner = winner
    m.finished = True
    db.record_match(CONN, m.lang, [(a, NAMES.get(a, "player")), (b, NAMES.get(b, "player"))], [ta, tb], winner)
    CONN.commit()


def _match_view(uid):
    mid = USER_MATCH.get(uid)
    m = MATCHES.get(mid) if mid else None
    if m is None:
        return None
    _tick(m)
    opp = m.other(uid)
    secs_left = max(0, int(m.ends - time.time())) if m.active else None
    view = {
        "match_id": m.id,
        "lang": m.lang,
        "round": m.round_no,
        "rounds": ROUNDS,
        "active": m.active,
        "letters": m.letters if m.active else [],
        "seconds_left": secs_left,
        "next_round_in": max(0, int(m.next_at - time.time())) if (not m.active and not m.finished) else None,
        "me": {"name": NAMES.get(uid, "you"), "total": m.totals[uid],
               "word": (m.best.get(uid) or (None,))[0] if m.active else None},
        "opponent": {"name": NAMES.get(opp, "opponent"), "total": m.totals[opp]},
        "history": [{"n": h["n"], "mine": h["words"][uid], "theirs": h["words"][opp],
                     "my_pts": h["pts"][uid], "their_pts": h["pts"][opp]} for h in m.history],
        "finished": m.finished,
        "result": None,
    }
    if m.finished:
        if m.winner == "void":
            view["result"] = "void"
        elif m.winner is None:
            view["result"] = "draw"
        else:
            view["result"] = "win" if m.winner == uid else "lose"
    return view


def _auth(session: str | None) -> int:
    uid = SESSIONS.get(session or "")
    if uid is None:
        raise HTTPException(401, "not logged in")
    return uid


# ---- config & auth ----

@app.get("/api/config")
def config():
    return {"sandbox": SANDBOX, "payments_enabled": PAYMENTS_ENABLED,
            "entry_fee_pi": ENTRY_FEE_PI, "memo": ENTRY_MEMO, "langs": list(WORDS.keys())}


class AuthIn(BaseModel):
    accessToken: str
    ref: str | None = None


@app.post("/api/auth")
def auth(body: AuthIn):
    r = httpx.get(f"{PI_API_BASE}/me", headers={"Authorization": f"Bearer {body.accessToken}"}, timeout=15)
    if r.status_code != 200:
        raise HTTPException(401, "pi token rejected")
    me = r.json()
    pi_uid = me.get("uid")
    username = me.get("username") or pi_uid
    if not pi_uid:
        raise HTTPException(401, "no uid from pi")
    with LOCK:
        uid = internal_id(pi_uid)
        CONN.execute("INSERT OR IGNORE INTO pi_users (internal_id, pi_uid, username) VALUES (?, ?, ?)",
                     (uid, pi_uid, username))
        NAMES[uid] = username
        ref_uid = None
        if body.ref:
            ref_uid = internal_id(body.ref) if body.ref != pi_uid else None
        status = db.capture_referral(CONN, uid, username, ref_uid)
        session = secrets.token_urlsafe(24)
        SESSIONS[session] = uid
    return {"session": session, "username": username, "referral": status,
            "ref_link_param": pi_uid}


# ---- matchmaking & duel ----

class PlayIn(BaseModel):
    lang: str = "en"
    payment_id: str | None = None


@app.post("/api/play")
def play(body: PlayIn, x_session: str | None = Header(default=None)):
    uid = _auth(x_session)
    if body.lang not in WORDS:
        raise HTTPException(400, "language not available")
    with LOCK:
        cur = _match_view(uid)
        if cur and not cur["finished"]:
            return {"status": "playing", "match": cur}
        USER_MATCH.pop(uid, None)
        if PAYMENTS_ENABLED:
            row = CONN.execute("SELECT * FROM pi_payments WHERE payment_id = ?", (body.payment_id or "",)).fetchone()
            if not row or row["status"] != "completed" or row["used"] or row["pi_uid"] != _pi_uid_of(uid):
                raise HTTPException(402, "entry payment required")
            CONN.execute("UPDATE pi_payments SET used = 1 WHERE payment_id = ?", (row["payment_id"],))
            db.record_entry(CONN, uid, ENTRY_FEE_PI)
        if uid in QUEUE[body.lang]:
            return {"status": "queued"}
        # another player is waiting in the same language -> pair them
        waiting = [q for q in QUEUE[body.lang] if q != uid]
        if waiting:
            opp = waiting[0]
            QUEUE[body.lang].remove(opp)
            m = Match(body.lang, opp, uid)
            MATCHES[m.id] = m
            USER_MATCH[opp] = m.id
            USER_MATCH[uid] = m.id
            _tick(m)
            return {"status": "playing", "match": _match_view(uid)}
        QUEUE[body.lang].append(uid)
        return {"status": "queued"}


def _pi_uid_of(uid: int) -> str:
    row = CONN.execute("SELECT pi_uid FROM pi_users WHERE internal_id = ?", (uid,)).fetchone()
    return row["pi_uid"] if row else ""


class WordIn(BaseModel):
    word: str


@app.post("/api/word")
def word(body: WordIn, x_session: str | None = Header(default=None)):
    uid = _auth(x_session)
    with LOCK:
        m = MATCHES.get(USER_MATCH.get(uid) or -1)
        if m is None:
            raise HTTPException(409, "no match")
        _tick(m)
        if not m.active:
            return {"ok": False, "reason": "round_closed", "match": _match_view(uid)}
        ok, info, points = game.score_word(body.word, m.lang, m.seed_counter, VALID[m.lang])
        if not ok:
            return {"ok": False, "reason": info, "match": _match_view(uid)}
        cur = m.best.get(uid)
        if cur is None or points > cur[1]:
            m.best[uid] = (info, points)
            return {"ok": True, "word": info, "points": points, "best": True, "match": _match_view(uid)}
        return {"ok": True, "word": info, "points": points, "best": False, "match": _match_view(uid)}


@app.post("/api/leave")
def leave(x_session: str | None = Header(default=None)):
    uid = _auth(x_session)
    with LOCK:
        for l in LANGS:
            if uid in QUEUE[l]:
                QUEUE[l].remove(uid)
    return {"ok": True}


@app.get("/api/state")
def state(x_session: str | None = Header(default=None)):
    uid = _auth(x_session)
    with LOCK:
        m = _match_view(uid)
        if m:
            return {"status": "finished" if m["finished"] else "playing", "match": m}
        queued = any(uid in q for q in QUEUE.values())
        return {"status": "queued" if queued else "idle", "match": None}


@app.get("/api/leaderboard")
def leaderboard():
    rows = db.leaderboard(CONN, 10)
    return {"rows": [{"name": r["name"], "matches": r["matches"], "wins": r["wins"], "points": r["points"]}
                     for r in rows]}


@app.get("/api/referral")
def referral(x_session: str | None = Header(default=None)):
    uid = _auth(x_session)
    with LOCK:
        counts, earned = db.referral_summary(CONN, uid)
        row = CONN.execute("SELECT pi_uid FROM pi_users WHERE internal_id = ?", (uid,)).fetchone()
    pct = {1: "5%", 2: "3%", 3: "2%"}
    return {
        "ref_param": row["pi_uid"] if row else "",
        "levels": [{"level": l, "share": pct[l], "people": counts[l],
                    "pending_pi": round(earned[l] / 1_000_000, 6)} for l in (1, 2, 3)],
        "total_pending_pi": round(sum(earned.values()) / 1_000_000, 6),
    }


# ---- Pi payments (SDK double-check flow: approve -> client signs -> complete) ----

def _pi_headers():
    return {"Authorization": f"Key {PI_APP_SECRET}", "Content-Type": "application/json"}


def _require_payments():
    if not PAYMENTS_ENABLED:
        raise HTTPException(503, "payments are not enabled on this server (set PI_APP_ID, PI_APP_SECRET, PI_ENV)")


class PayIn(BaseModel):
    paymentId: str
    txid: str | None = None


@app.post("/api/payments/approve")
def pay_approve(body: PayIn, x_session: str | None = Header(default=None)):
    uid = _auth(x_session)
    _require_payments()
    with LOCK:
        pi_uid = _pi_uid_of(uid)
    pr = httpx.get(f"{PI_API_BASE}/payments/{body.paymentId}", headers=_pi_headers(), timeout=20)
    if pr.status_code != 200:
        raise HTTPException(502, "could not fetch payment from pi")
    p = pr.json()
    # never approve a payment that is not this user's entry fee
    if p.get("user_uid") != pi_uid or abs(float(p.get("amount", 0)) - ENTRY_FEE_PI) > 1e-9 \
            or p.get("memo") != ENTRY_MEMO:
        raise HTTPException(400, "payment does not match this entry")
    ar = httpx.post(f"{PI_API_BASE}/payments/{body.paymentId}/approve", headers=_pi_headers(), timeout=20)
    if ar.status_code not in (200, 201):
        raise HTTPException(502, "pi approve failed")
    with LOCK:
        CONN.execute("INSERT OR REPLACE INTO pi_payments (payment_id, pi_uid, amount, status) VALUES (?, ?, ?, 'approved')",
                     (body.paymentId, pi_uid, ENTRY_FEE_PI))
        CONN.commit()
    return {"ok": True}


@app.post("/api/payments/complete")
def pay_complete(body: PayIn, x_session: str | None = Header(default=None)):
    uid = _auth(x_session)
    _require_payments()
    if not body.txid:
        raise HTTPException(400, "txid required")
    cr = httpx.post(f"{PI_API_BASE}/payments/{body.paymentId}/complete", headers=_pi_headers(),
                    json={"txid": body.txid}, timeout=20)
    if cr.status_code not in (200, 201):
        raise HTTPException(502, "pi complete failed")
    with LOCK:
        CONN.execute("UPDATE pi_payments SET status = 'completed', txid = ? WHERE payment_id = ? AND pi_uid = ?",
                     (body.txid, body.paymentId, _pi_uid_of(uid)))
        CONN.commit()
    return {"ok": True, "payment_id": body.paymentId}


@app.post("/api/payments/incomplete")
def pay_incomplete(body: PayIn, x_session: str | None = Header(default=None)):
    """Called when the SDK reports an unfinished payment from an earlier session."""
    return pay_complete(body, x_session) if body.txid else {"ok": False, "reason": "no txid to complete"}


# ---- pages & static ----

app.mount("/static", StaticFiles(directory=str(HERE / "static")), name="static")


def _page(name):
    return FileResponse(str(HERE / "static" / name))


@app.get("/")
def home():
    return _page("index.html")


@app.get("/match")
def match_page():
    return _page("match.html")


@app.get("/duel")
def duel_page():
    return _page("duel.html")


@app.get("/leaderboard")
def leaderboard_page():
    return _page("leaderboard.html")


@app.get("/referral")
def referral_page():
    return _page("referral.html")


@app.get("/health")
def health():
    return {"ok": True}
