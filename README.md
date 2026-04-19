# ai-digest-bot

AI-powered bot that curates tech & AI news and delivers a personalized Spanish newsletter via Telegram, twice a week.

## What it does

- Fetches tech and AI news from RSS feeds every Wednesday and Sunday
- Filters and prioritizes news with **real-world impact** for end users (no academic or purely technical articles)
- Uses Claude to generate a **newsletter in Spanish** ready to read
- Delivers everything via **Telegram** automatically at 9:00 AM

## Requirements

- Python 3.11+
- Anthropic API Key (Claude) — [console.anthropic.com](https://console.anthropic.com)
- Telegram Bot + Chat ID

## Installation

```bash
# 1. Clone or download the project
cd ai-digest-bot

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env and fill in the three values
```

## Environment variables (`.env`)

| Variable | Description |
|---|---|
| `ANTHROPIC_API_KEY` | Anthropic API Key |
| `TELEGRAM_BOT_TOKEN` | Telegram bot token (from @BotFather) |
| `TELEGRAM_CHAT_ID` | ID of the chat where messages will be sent |

### Getting the Telegram Chat ID

1. Start a conversation with your bot on Telegram.
2. Visit: `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
3. Look for the `"chat": {"id": ...}` field — that number is your `TELEGRAM_CHAT_ID`.

## Configuration (`config.py`)

| Variable | Description | Default |
|---|---|---|
| `ARTICLES_PER_FEED` | Max articles fetched per feed | `5` |
| `MAX_ARTICLES_TOTAL` | Total articles kept after filtering | `20` |
| `LINKEDIN_POSTS_COUNT` | LinkedIn post templates per run | `3` |
| `RSS_FEEDS` | RSS sources grouped by category | see below |
| `TOPICS_OF_INTEREST` | Topics Claude will prioritize | see below |

### Default RSS sources

| Category | Sources |
|---|---|
| Consumer AI | OpenAI Blog, The Verge, TechCrunch |
| Everyday tech | CNET, Wired, Ars Technica |
| Productivity & AI tools | Lifehacker, Zapier Blog, Hugging Face |
| Hacker News | Hacker News RSS |

### Article selection criteria

Claude actively filters to include only news where the end user sees a concrete and immediate benefit:
- New AI features in well-known apps (Google, Apple, Meta, ChatGPT...)
- AI applied to health, education, work, home, or entertainment
- AI productivity tools for non-technical users

Excluded: academic papers, benchmarks, infrastructure improvements, and technical jargon.

## Scheduling

The pipeline runs automatically via **GitHub Actions** every Wednesday and Sunday at 08:00 UTC (09:00 CET / 10:00 CEST). No server required.

To trigger it manually: go to **Actions → Newsletter Digest → Run workflow** in GitHub.

## Project structure

```
.
├── main.py                 # Pipeline orchestrator
├── config.py               # All configuration in one place
├── requirements.txt
├── .env.example            # Environment variables template
├── .github/
│   └── workflows/
│       └── newsletter.yml  # GitHub Actions cron schedule
├── sources/
│   └── rss_fetcher.py      # RSS article fetcher (last 7 days)
├── ai/
│   └── content_gen.py      # Newsletter generation with Claude
└── delivery/
    └── telegram_bot.py     # Telegram Bot API delivery
```