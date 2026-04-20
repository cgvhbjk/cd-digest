import requests

import config

SLACK_API_URL = "https://slack.com/api/chat.postMessage"
MAX_SLACK_CHARS = 3000


def post_digest(text: str) -> None:
    """Post digest to Slack, splitting into chunks if needed."""
    if not config.SLACK_BOT_TOKEN:
        raise ValueError("SLACK_BOT_TOKEN not set in environment.")
    if not config.SLACK_CHANNEL_ID:
        raise ValueError("SLACK_CHANNEL_ID not set in environment.")

    chunks = _split(text)
    for chunk in chunks:
        _post(chunk)


def _post(text: str) -> None:
    response = requests.post(
        SLACK_API_URL,
        headers={"Authorization": f"Bearer {config.SLACK_BOT_TOKEN}"},
        json={"channel": config.SLACK_CHANNEL_ID, "text": text},
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()
    if not data.get("ok"):
        raise RuntimeError(f"Slack API error: {data.get('error')}")


def _split(text: str) -> list[str]:
    if len(text) <= MAX_SLACK_CHARS:
        return [text]
    chunks, current = [], []
    current_len = 0
    for line in text.splitlines(keepends=True):
        if current_len + len(line) > MAX_SLACK_CHARS and current:
            chunks.append("".join(current))
            current, current_len = [], 0
        current.append(line)
        current_len += len(line)
    if current:
        chunks.append("".join(current))
    return chunks
