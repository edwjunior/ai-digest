import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Claude model
CLAUDE_MODEL = "claude-sonnet-4-6"

# Schedule: day_of_week "wed,sun", hour and minute (24h format, local time)
SCHEDULE_DAYS = "wed,sun"
SCHEDULE_HOUR = 9
SCHEDULE_MINUTE = 0

# How many articles to fetch per feed and how many to keep after filtering
ARTICLES_PER_FEED = 5
MAX_ARTICLES_TOTAL = 20

# RSS feeds grouped by topic
RSS_FEEDS = {
    "IA para el consumidor": [
        "https://openai.com/news/rss.xml",
        "https://www.theverge.com/rss/index.xml",
        "https://feeds.feedburner.com/TechCrunch",
    ],
    "Tech cotidiana": [
        "https://www.cnet.com/rss/news/",
        "https://www.wired.com/feed/rss",
        "https://feeds.arstechnica.com/arstechnica/index",
    ],
    "Productividad & Herramientas IA": [
        "https://lifehacker.com/feed/rss",
        "https://zapier.com/blog/feeds/latest/",
        "https://huggingface.co/blog/feed.xml",
    ],
    "Hacker News": [
        "https://news.ycombinator.com/rss",
    ],
}

# Topics Claude will focus on when selecting and summarizing
TOPICS_OF_INTEREST = [
    "aplicaciones de IA para el usuario final",
    "herramientas de IA que cualquier persona puede usar hoy",
    "IA en salud, educación, trabajo, hogar o entretenimiento",
    "nuevas apps o funciones de IA en productos conocidos (Google, Apple, Meta, etc.)",
    "cómo la IA está cambiando la vida cotidiana",
    "herramientas de productividad con IA para no técnicos",
    "robots, asistentes de voz, IA en el móvil",
]

# Number of LinkedIn post templates to generate
LINKEDIN_POSTS_COUNT = 3
