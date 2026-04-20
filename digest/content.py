import config


def build_thread_text(thread_data: dict) -> str:
    """Extract original post + top replies into a single text block."""
    posts = thread_data.get("post_stream", {}).get("posts", [])
    if not posts:
        return ""

    parts = []

    # Original post
    parts.append(f"[Original Post]\n{posts[0].get('cooked', '')}")

    # First 5 replies
    early_replies = posts[1:6]
    for p in early_replies:
        parts.append(f"[Reply]\n{p.get('cooked', '')}")

    # Top 3 replies by likes (excluding original post)
    remaining = sorted(posts[1:], key=lambda p: p.get("like_count", 0), reverse=True)
    for p in remaining[:3]:
        if p not in early_replies:
            parts.append(f"[Top Reply]\n{p.get('cooked', '')}")

    text = "\n\n---\n\n".join(parts)
    return text[: config.MAX_THREAD_CHARS]
