# ai-digest-bot

AI-powered bot that curates tech & AI news and delivers a personalized Spanish newsletter + LinkedIn post templates via Telegram, twice a week.

## ¿Qué hace?

- Recopila noticias de tecnología e IA desde fuentes RSS cada miércoles y domingo
- Filtra y prioriza noticias con **impacto cotidiano** para el usuario final (no noticias técnicas ni académicas)
- Genera con Claude una **newsletter en español** lista para leer
- Genera **plantillas de posts para LinkedIn** con tono informal y opinión personal
- Envía todo por **Telegram** automáticamente a las 9:00h

## Requisitos

- Python 3.11+
- API Key de Anthropic (Claude) — [console.anthropic.com](https://console.anthropic.com)
- Bot de Telegram + Chat ID

## Instalación

```bash
# 1. Clona o descarga el proyecto
cd ai-digest-bot

# 2. Crea un entorno virtual
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

# 3. Instala dependencias
pip install -r requirements.txt

# 4. Configura las variables de entorno
cp .env.example .env
# Edita .env con tu editor y rellena los tres valores
```

## Variables de entorno (`.env`)

| Variable | Descripción |
|---|---|
| `ANTHROPIC_API_KEY` | API Key de Anthropic |
| `TELEGRAM_BOT_TOKEN` | Token del bot de Telegram (de @BotFather) |
| `TELEGRAM_CHAT_ID` | ID del chat donde se enviarán los mensajes |

### Obtener el Telegram Chat ID

1. Inicia una conversación con tu bot en Telegram.
2. Visita: `https://api.telegram.org/bot<TU_TOKEN>/getUpdates`
3. Busca el campo `"chat": {"id": ...}` — ese número es tu `TELEGRAM_CHAT_ID`.

## Configuración (`config.py`)

| Variable | Descripción | Default |
|---|---|---|
| `SCHEDULE_DAYS` | Días de envío | `"wed,sun"` |
| `SCHEDULE_HOUR` | Hora de envío (24h, zona Madrid) | `9` |
| `ARTICLES_PER_FEED` | Artículos máximos por feed | `5` |
| `MAX_ARTICLES_TOTAL` | Artículos totales tras filtrar | `20` |
| `LINKEDIN_POSTS_COUNT` | Plantillas LinkedIn por envío | `3` |
| `RSS_FEEDS` | Fuentes RSS agrupadas por categoría | ver abajo |
| `TOPICS_OF_INTEREST` | Temas que Claude priorizará | ver abajo |

### Fuentes RSS por defecto

| Categoría | Fuentes |
|---|---|
| IA para el consumidor | OpenAI Blog, The Verge, TechCrunch |
| Tech cotidiana | CNET, Wired, Ars Technica |
| Productividad & Herramientas IA | Lifehacker, Zapier Blog, Hugging Face |
| Hacker News | Hacker News RSS |

### Criterio de selección de noticias

Claude filtra activamente para incluir solo noticias donde el usuario final ve un beneficio concreto e inmediato:
- Nuevas funciones de IA en apps conocidas (Google, Apple, Meta, ChatGPT...)
- IA aplicada a salud, educación, trabajo, hogar o entretenimiento
- Herramientas de productividad con IA para no técnicos

Se descartan: papers académicos, benchmarks, mejoras de infraestructura y jerga técnica.

## Uso

```bash
# Prueba puntual (ejecuta el pipeline ahora mismo)
python main.py --now

# Modo scheduler (ejecuta automáticamente miércoles y domingos a las 9:00h)
python main.py
```

## Estructura del proyecto

```
.
├── main.py                 # Orquestador + scheduler (APScheduler)
├── config.py               # Toda la configuración en un sitio
├── requirements.txt
├── .env.example            # Plantilla de variables de entorno
├── sources/
│   └── rss_fetcher.py      # Fetch de artículos RSS (últimos 7 días)
├── ai/
│   └── content_gen.py      # Generación de newsletter y posts con Claude
└── delivery/
    └── telegram_bot.py     # Envío por Telegram Bot API
```
