import httpx
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"
MAX_MESSAGE_LENGTH = 4096


def _send_message(text: str, parse_mode: str = "Markdown") -> bool:
    try:
        response = httpx.post(
            f"{TELEGRAM_API}/sendMessage",
            json={
                "chat_id": TELEGRAM_CHAT_ID,
                "text": text,
                "parse_mode": parse_mode,
                "disable_web_page_preview": False,
            },
            timeout=15,
        )
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"[telegram] Error sending message: {e}")
        return False


def _split_message(text: str) -> list[str]:
    if len(text) <= MAX_MESSAGE_LENGTH:
        return [text]

    chunks = []
    while text:
        if len(text) <= MAX_MESSAGE_LENGTH:
            chunks.append(text)
            break
        # Split at last newline before the limit
        split_at = text.rfind("\n", 0, MAX_MESSAGE_LENGTH)
        if split_at == -1:
            split_at = MAX_MESSAGE_LENGTH
        chunks.append(text[:split_at])
        text = text[split_at:].lstrip("\n")
    return chunks


def send_newsletter(newsletter_text: str) -> None:
    header = "📰 *TECHPULSE NEWSLETTER*\n\n"
    full_text = header + newsletter_text

    chunks = _split_message(full_text)
    for i, chunk in enumerate(chunks):
        success = _send_message(chunk)
        if success:
            print(f"[telegram] Newsletter chunk {i+1}/{len(chunks)} sent.")
        else:
            print(f"[telegram] Failed to send newsletter chunk {i+1}.")


def send_linkedin_posts(posts: list[str]) -> None:
    intro = (
        "💼 *PLANTILLAS PARA LINKEDIN*\n"
        "Copia y pega la que más te guste directamente en LinkedIn.\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
    )
    _send_message(intro)

    for i, post in enumerate(posts, 1):
        message = f"*Post {i} de {len(posts)}:*\n\n{post}"
        success = _send_message(message, parse_mode="Markdown")
        if success:
            print(f"[telegram] LinkedIn post {i}/{len(posts)} sent.")
        else:
            # Retry without markdown in case of formatting issues
            _send_message(f"Post {i} de {len(posts)}:\n\n{post}", parse_mode="")
