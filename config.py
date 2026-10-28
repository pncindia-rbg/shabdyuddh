"""Settings, read from environment (or .env next to this file)."""
import os
from pathlib import Path

try:
    from dotenv import load_dotenv

    load_dotenv(Path(__file__).resolve().parent / ".env")
except ImportError:
    pass

BASE = Path(__file__).resolve().parent

BOT_TOKEN = os.environ.get("BOT_TOKEN", "").strip()
DB_PATH = os.environ.get("DB_PATH", str(BASE / "shabdyuddh.db"))
ROUND_SECONDS = int(os.environ.get("ROUND_SECONDS", "60"))
ROUNDS = int(os.environ.get("ROUNDS", "5"))
BOT_USERNAME = os.environ.get("BOT_USERNAME", "shabdyudh_bot").lstrip("@")  # for referral links
ENTRY_FEE_PI = float(os.environ.get("ENTRY_FEE_PI", "0.5"))  # stub only, not charged for real

WORD_FILES = {
    "en": str(BASE / "words" / "en.txt"),
    "hi": str(BASE / "words" / "hi.txt"),
    "vi": str(BASE / "words" / "vi.txt"),
    "id": str(BASE / "words" / "id.txt"),
    "ar": str(BASE / "words" / "ar.txt"),
}
