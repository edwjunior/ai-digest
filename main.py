import logging
from sources.rss_fetcher import fetch_all_articles
from ai.content_gen import generate_newsletter, generate_linkedin_posts
from delivery.telegram_bot import send_newsletter, send_linkedin_posts

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)


def main() -> None:
    log.info("=== Iniciando pipeline de newsletter ===")

    log.info("Paso 1/4: Obteniendo artículos RSS...")
    articles = fetch_all_articles()
    if not articles:
        log.warning("No se encontraron artículos. Abortando.")
        return
    log.info(f"  → {len(articles)} artículos obtenidos.")

    log.info("Paso 2/4: Generando newsletter con Claude...")
    newsletter = generate_newsletter(articles)
    log.info("  → Newsletter generada.")

    log.info("Paso 3/4: Generando posts de LinkedIn con Claude...")
    linkedin_posts = generate_linkedin_posts(articles)
    log.info(f"  → {len(linkedin_posts)} posts generados.")

    log.info("Paso 4/4: Enviando por Telegram...")
    send_newsletter(newsletter)
    send_linkedin_posts(linkedin_posts)
    log.info("  → Envío completado.")

    log.info("=== Pipeline finalizado con éxito ===")


if __name__ == "__main__":
    main()
