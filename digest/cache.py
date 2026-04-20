import json
import os
from datetime import date

import config


def load_cache() -> dict:
    if not os.path.exists(config.CACHE_PATH):
        return {}
    with open(config.CACHE_PATH) as f:
        return json.load(f)


def save_cache(cache: dict) -> None:
    os.makedirs(os.path.dirname(config.CACHE_PATH), exist_ok=True)
    with open(config.CACHE_PATH, "w") as f:
        json.dump(cache, f, indent=2)


def should_process(thread: dict, cache: dict) -> bool:
    tid = str(thread["id"])
    if tid not in cache:
        return True
    return thread["reply_count"] > cache[tid]["last_reply_count"]


def update_cache(cache: dict, thread: dict, summary: str) -> None:
    cache[str(thread["id"])] = {
        "last_reply_count": thread["reply_count"],
        "summary": summary,
        "last_processed": str(date.today()),
    }
