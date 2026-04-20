import config


def is_valid_thread(thread: dict) -> bool:
    tags = thread["tags"]
    title = thread["title"].lower()

    if any(tag in config.BLOCKED_TAGS for tag in tags):
        return False

    if not any(tag in config.TECH_TAGS for tag in tags):
        return False

    if any(word in title for word in config.BLOCKED_KEYWORDS):
        return False

    return True


def score_thread(thread: dict) -> float:
    score = (
        2 * thread["reply_count"]
        + 3 * thread["like_count"]
        + thread["views"] / 50
    )
    if any(tag in ["programming", "controls"] for tag in thread["tags"]):
        score *= 1.2
    return score


def filter_and_rank(threads: list[dict]) -> list[dict]:
    valid = [t for t in threads if is_valid_thread(t)]
    return sorted(valid, key=score_thread, reverse=True)
