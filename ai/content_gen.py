import anthropic
from datetime import datetime
from config import ANTHROPIC_API_KEY, CLAUDE_MODEL, TOPICS_OF_INTEREST, LINKEDIN_POSTS_COUNT

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


def _articles_to_text(articles: list[dict]) -> str:
    lines = []
    for i, a in enumerate(articles, 1):
        lines.append(
            f"{i}. [{a['topic']}] {a['title']}\n"
            f"   Fuente: {a['source']} | Fecha: {a['published']}\n"
            f"   URL: {a['url']}\n"
            f"   Resumen: {a['summary']}\n"
        )
    return "\n".join(lines)


def generate_newsletter(articles: list[dict]) -> str:
    today = datetime.now().strftime("%A, %d de %B de %Y")
    topics_str = ", ".join(TOPICS_OF_INTEREST)
    articles_text = _articles_to_text(articles)

    prompt = f"""Eres el editor de una newsletter semanal de tecnología en español llamada **TechPulse**.
Hoy es {today}.

Tu misión es acercar la tecnología a personas de a pie: gente que no es técnica pero quiere entender cómo la IA y la tecnología están cambiando su vida cotidiana.

Tu tarea es crear una newsletter completa, curada y en español a partir de los artículos que te doy a continuación.
Los temas de interés son: {topics_str}.

ARTÍCULOS DISPONIBLES:
{articles_text}

CRITERIO DE SELECCIÓN (muy importante):
- Prioriza noticias donde el usuario final puede ver un beneficio concreto e inmediato.
- Descarta noticias puramente técnicas, de investigación académica o de infraestructura (modelos base, benchmarks, arquitecturas de redes neuronales, etc.) a menos que tengan un impacto directo en productos reales.
- Ejemplos de lo que SÍ incluir: nueva función de IA en WhatsApp, app que usa IA para algo del hogar, IA que ayuda con la salud, ChatGPT añade X funcionalidad, etc.
- Ejemplos de lo que NO incluir: paper sobre un nuevo modelo, mejoras en CUDA, comparativas de benchmarks.

INSTRUCCIONES:
- Escribe la newsletter completamente en español (traduce títulos si es necesario).
- Selecciona los 6-8 artículos más relevantes según el criterio anterior.
- Explica siempre el "¿y esto para qué me sirve a mí?" de cada noticia.
- Estructura:
  1. **Cabecera**: saludo breve y frase gancho sobre la semana tech.
  2. **Noticia destacada**: la noticia con mayor impacto para el usuario final, con 3-4 líneas de contexto y un ejemplo concreto de cómo afecta al día a día.
  3. **En resumen**: lista de 5-7 noticias con título, 2-3 líneas de resumen en lenguaje no técnico y enlace.
  4. **Reflexión de cierre**: 2-3 líneas tuyas (tono cercano, no corporativo) sobre la tendencia de la semana.
  5. **Pie**: firma "TechPulse Newsletter" y "Hasta el próximo número 👋".

- Tono: cercano, divulgativo, como si se lo explicaras a un amigo no técnico.
- Usa emojis con moderación para dar vida al texto.
- Evita palabras como "algoritmo", "modelo", "parámetros", "inferencia", "token" o cualquier jerga técnica.
- Formatea para Telegram: usa *negrita* con asteriscos, _cursiva_ con guiones bajos, y saltos de línea claros.
- NO incluyas artículos irrelevantes solo para rellenar.

Genera únicamente el contenido de la newsletter, sin explicaciones adicionales."""

    message = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=2500,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


def generate_linkedin_posts(articles: list[dict]) -> list[str]:
    articles_text = _articles_to_text(articles)
    topics_str = ", ".join(TOPICS_OF_INTEREST)

    prompt = f"""Eres un creador de contenido en LinkedIn con voz auténtica e informal.
Tu audiencia es amplia: profesionales de cualquier sector que no son técnicos pero están curiosos por cómo la IA está cambiando su trabajo y su vida diaria.

A partir de los siguientes artículos tech recientes, genera exactamente {LINKEDIN_POSTS_COUNT} publicaciones de LinkedIn DIFERENTES entre sí.
Los temas de interés son: {topics_str}.

ARTÍCULOS DISPONIBLES:
{articles_text}

CRITERIO DE SELECCIÓN:
- Elige noticias donde el impacto sea concreto y visible para cualquier persona, no solo para técnicos.
- El lector debe pensar "esto me afecta a mí" o "esto lo puedo usar ya".

INSTRUCCIONES PARA CADA POST:
- Tono: informal, directo, con opinión personal (usa "yo creo", "me parece", "esto me llama la atención").
- Escribe como si hablaras con un compañero de trabajo, no como un experto dando clase.
- Cada post debe basarse en UNA noticia o tema concreto de los artículos.
- Incluye siempre un ejemplo cotidiano o analogía simple para explicar el impacto.
- Estructura sugerida para cada post:
  * Gancho (1-2 líneas que enganchen desde el principio, algo que sorprenda o genere curiosidad)
  * Explica qué ha pasado y por qué importa en lenguaje sencillo (3-5 líneas)
  * Tu opinión honesta + pregunta al lector para generar conversación (1-2 líneas)
  * 3-5 hashtags relevantes al final
- Longitud: entre 150-250 palabras por post.
- Evita sonar corporativo o como un comunicado de prensa.
- Evita jerga técnica: no uses palabras como "modelo", "algoritmo", "parámetros", "LLM", etc.
- Usa saltos de línea para dar ritmo al texto (como en LinkedIn real).
- NO uses markdown con asteriscos para negrita, escribe texto plano como en LinkedIn.

FORMATO DE RESPUESTA:
Devuelve los {LINKEDIN_POSTS_COUNT} posts separados por esta línea exacta entre cada uno:
---POST---

Genera únicamente los posts, sin numerarlos ni añadir explicaciones."""

    message = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = message.content[0].text
    posts = [p.strip() for p in raw.split("---POST---") if p.strip()]
    return posts
