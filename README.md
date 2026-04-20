# cd-digest

A daily digest of high-quality technical discussions from [Chief Delphi](https://www.chiefdelphi.com), filtered, scored, summarized by a local LLM, and posted to Slack.

---

## How it works

```
fetch_threads (Discourse API)
   ↓
hard_filter (blocked tags + blocked keywords)
   ↓
score_threads (replies × 2 + likes × 3 + views / 50)
   ↓
select top N
   ↓
check cache (skip unchanged threads)
   ↓
fetch full thread content
   ↓
summarize via local LLM
   ↓
format digest
   ↓
post to Slack
   ↓
update cache
```

Only threads tagged with recognized technical tags (`programming`, `autonomous`, `cad`, `vision`, etc.) pass the filter. Social, build-blog, reveal, and meme threads are explicitly blocked.

---

## Setup

### 1. Clone and install

```bash
git clone https://github.com/cgvhbjk/cd-digest.git
cd cd-digest
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
```

Edit `.env`:

```
SLACK_BOT_TOKEN=xoxb-your-token-here
SLACK_CHANNEL_ID=C0XXXXXXXXX
```

Both are optional for a dry run — the digest will print to stdout and skip Slack if they're missing.

---

## LLM Setup (Ollama)

The summarizer stub is in `digest/summarizer.py`. Any local LLM works — Ollama is recommended.

**Install Ollama:** https://ollama.com

**Pull a model:**

| Hardware | Recommended model | Command |
|---|---|---|
| GPU with 8GB+ VRAM | llama3.1:8b | `ollama pull llama3.1:8b` |
| GPU with 4–6GB VRAM | phi3:mini | `ollama pull phi3:mini` |
| CPU only | llama3.2:3b | `ollama pull llama3.2:3b` |

**Wire it in** — open `digest/summarizer.py` and replace the `raise NotImplementedError` with:

```python
import requests
response = requests.post(
    "http://localhost:11434/api/generate",
    json={"model": "llama3.1:8b", "prompt": prompt, "stream": False},
    timeout=120,
)
return response.json()["response"].strip()
```

The Ollama skeleton is already present in the file as a comment — just uncomment it.

---

## Slack Setup

1. Go to [api.slack.com/apps](https://api.slack.com/apps) → **Create New App** → From scratch
2. Under **OAuth & Permissions** → Scopes → add `chat:write`
3. **Install to Workspace** → copy the **Bot User OAuth Token** (`xoxb-...`)
4. Invite the bot to your channel: `/invite @your-bot-name`
5. Get the channel ID: right-click the channel → **View channel details** → copy the ID at the bottom
6. Add both values to your `.env` file

---

## Running

```bash
python main.py
```

On first run, output will look like:

```
Fetching recent threads...
  99 threads found in last 24h
  16 threads passed technical filter
  7 threads to process (new or updated)
  Summarizing: Introducing BLine: A New Rapid Polyline...
  ...

--- Digest Preview ---
Chief Delphi Technical Digest (04/20/2026)
...
```

---

## Scheduling

### GitHub Actions (recommended — no local machine needed)

The included workflow runs daily at 9:00 AM ET. To enable it:

1. Push the repo to GitHub (already done)
2. Go to **Settings → Secrets and variables → Actions**
3. Add secrets: `SLACK_BOT_TOKEN`, `SLACK_CHANNEL_ID`
4. If using a remote Ollama instance, also add `OLLAMA_HOST` and `OLLAMA_MODEL`
5. The workflow will run automatically — or trigger manually via **Actions → Daily Digest → Run workflow**

### Local (cron / Task Scheduler)

**macOS / Linux:**
```bash
# runs at 9 AM every day
0 9 * * * cd /path/to/cd-digest && python main.py
```

**Windows Task Scheduler:**
- Action: `python C:\path\to\cd-digest\main.py`
- Trigger: Daily at your preferred time

---

## Configuration

All tunables are in `config.py`:

| Variable | Default | Description |
|---|---|---|
| `TOP_N_THREADS` | 7 | Max threads per digest |
| `LOOKBACK_HOURS` | 24 | How far back to look |
| `MAX_THREAD_CHARS` | 9000 | Max chars sent to LLM per thread |
| `TECH_TAGS` | see file | Tags that qualify a thread as technical |
| `BLOCKED_TAGS` | see file | Tags that immediately disqualify a thread |
| `BLOCKED_KEYWORDS` | see file | Title keywords that disqualify a thread |

If non-technical threads slip through, add their tags to `BLOCKED_TAGS` or keywords to `BLOCKED_KEYWORDS` — no ML needed.

---

## Project structure

```
cd-digest/
├── main.py                  # entry point
├── config.py                # all tunables and env vars
├── requirements.txt
├── .env.example
├── .github/
│   └── workflows/
│       └── daily_digest.yml # GitHub Actions schedule
├── digest/
│   ├── fetcher.py           # Discourse API (fetch latest + full threads)
│   ├── filter.py            # hard filter + scoring
│   ├── cache.py             # seen_threads.json read/write
│   ├── content.py           # extracts post text for LLM
│   ├── summarizer.py        # LLM interface — wire in your model here
│   ├── formatter.py         # builds the Slack message string
│   └── slack.py             # posts to Slack API
└── data/
    └── seen_threads.json    # auto-created, gitignored
```
