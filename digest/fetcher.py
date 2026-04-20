import time
from datetime import datetime, timezone, timedelta
from typing import Optional
import requests

import config


def _get(url: str, params: Optional[dict] = None) -> dict:
    response = requests.get(url, params=params, timeout=15)
    response.raise_for_status()
    return response.json()


def fetch_recent_threads() -> list[dict]:
    """Return threads posted or active in the last LOOKBACK_HOURS hours."""
    cutoff = datetime.now(timezone.utc) - timedelta(hours=config.LOOKBACK_HOURS)
    threads = []
    page = 0

    while True:
        data = _get(f"{config.DISCOURSE_BASE_URL}/latest.json", params={"page": page})
        topic_list = data.get("topic_list", {})
        topics = topic_list.get("topics", [])

        if not topics:
            break

        found_any_recent = False
        for topic in topics:
            bumped_at = topic.get("bumped_at") or topic.get("created_at")
            if not bumped_at:
                continue
            ts = datetime.fromisoformat(bumped_at.replace("Z", "+00:00"))
            if ts >= cutoff:
                found_any_recent = True
                threads.append({
                    "id": topic["id"],
                    "title": topic["title"],
                    "tags": topic.get("tags") or [],
                    "reply_count": topic.get("reply_count", 0),
                    "like_count": topic.get("like_count", 0),
                    "views": topic.get("views", 0),
                    "slug": topic.get("slug", str(topic["id"])),
                })

        if not found_any_recent:
            break

        if not topic_list.get("more_topics_url"):
            break

        page += 1
        time.sleep(0.5)

    return threads


def fetch_full_thread(thread_id: int) -> dict:
    """Return the full thread JSON for a given topic id."""
    return _get(f"{config.DISCOURSE_BASE_URL}/t/{thread_id}.json")
