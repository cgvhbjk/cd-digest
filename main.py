import sys

import config
from digest.fetcher import fetch_recent_threads, fetch_full_thread
from digest.filter import filter_and_rank
from digest.cache import load_cache, save_cache, should_process, update_cache
from digest.content import build_thread_text
from digest.summarizer import summarize
from digest.formatter import format_digest
from digest.slack import post_digest


def run():
    print("Fetching recent threads...")
    threads = fetch_recent_threads()
    print(f"  {len(threads)} threads found in last {config.LOOKBACK_HOURS}h")

    ranked = filter_and_rank(threads)
    print(f"  {len(ranked)} threads passed technical filter")

    cache = load_cache()
    candidates = [t for t in ranked if should_process(t, cache)][: config.TOP_N_THREADS]
    print(f"  {len(candidates)} threads to process (new or updated)")

    if not candidates:
        print("Nothing new to digest today.")
        return

    results = []
    for thread in candidates:
        print(f"  Summarizing: {thread['title'][:60]}...")
        try:
            full = fetch_full_thread(thread["id"])
            text = build_thread_text(full)
            summary = summarize(text)
            update_cache(cache, thread, summary)
            results.append({"thread": thread, "summary": summary})
        except NotImplementedError as e:
            print(f"  [SKIP] {e}")
            results.append({"thread": thread, "summary": "[Summary pending — LLM not configured]"})
        except Exception as e:
            print(f"  [ERROR] {thread['title']}: {e}")

    digest = format_digest(results)
    print("\n--- Digest Preview ---")
    print(digest)

    try:
        post_digest(digest)
        print("\nPosted to Slack.")
    except ValueError as e:
        print(f"\n[Slack skipped] {e}")
    except Exception as e:
        print(f"\n[Slack error] {e}")

    save_cache(cache)
    print("Cache updated.")


if __name__ == "__main__":
    run()
