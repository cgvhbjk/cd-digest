from datetime import date

import config


def format_digest(threads_with_summaries: list[dict]) -> str:
    today = date.today().strftime("%m/%d/%Y")
    lines = [f"Chief Delphi Technical Digest ({today})\n"]

    for i, item in enumerate(threads_with_summaries, 1):
        thread = item["thread"]
        summary = item["summary"]
        url = f"{config.DISCOURSE_BASE_URL}/t/{thread['slug']}/{thread['id']}"

        lines.append("-" * 40)
        lines.append(f"{i}. {thread['title']}")
        lines.append(f"\n{summary}")
        lines.append(f"\nLink: {url}")
        lines.append("")

    return "\n".join(lines)
