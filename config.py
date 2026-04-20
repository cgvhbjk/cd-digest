import os
from dotenv import load_dotenv

load_dotenv()

DISCOURSE_BASE_URL = "https://www.chiefdelphi.com"
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_CHANNEL_ID = os.getenv("SLACK_CHANNEL_ID")

TOP_N_THREADS = 7
MAX_THREAD_CHARS = 9000
LOOKBACK_HOURS = 24

TECH_TAGS = [
    "programming", "electrical", "mechanical",
    "controls", "vision", "swerve",
    "software", "hardware",
]

BLOCKED_TAGS = [
    "offseason", "fun", "meme", "media",
    "community", "events", "announcements",
    "non-technical",
]

BLOCKED_KEYWORDS = [
    "favorite", "best team", "funniest",
    "meme", "prediction", "rank",
    "drama", "controversy",
]

CACHE_PATH = "data/seen_threads.json"
