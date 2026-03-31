import anthropic
import json
import os

def generar_contenido(noticia: dict, detalle: str = "") -> dict:
    """
    Recibe una noticia y genera:
    - guion_corto: para Reels/Shorts/TikTok (30-45 seg)
    - caption_instagram: texto + hashtags para Instagram
    - caption_tiktok: texto + hashtags para TikTok
    - caption_youtube: título + descripción para YouTube Shorts
    """
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    contexto = f"Título de la noticia: {noticia['titulo']}"
    if detalle:
        contexto += f"\n\nDetalle: {detalle}"

    prompt = f"""Sos el community manager de "Desde el Pogo", una página argentina de música que cubre rock, trap, cumbia, folklore y todo el ecosistema musical argentino. El tono es apasionado, directo, argento, como alguien que realmente vive la música. Nada corporativo, nada genérico.

{contexto}

Generá el siguiente contenido en formato JSON (solo el JSON, sin texto adicional):

{{
  "guion_corto": "Guion de 30-45 segundos para leer en cámara o usar como subtítulos en un Reel/TikTok/Short. Máximo 80 palabras. Arrancá con un gancho fuerte. Terminá con una pregunta o call to action para generar comentarios.",
  "caption_instagram": "Caption para Instagram. 2-3 oraciones con energía. Incluí 10 hashtags relevantes al final mezclando hashtags populares y de nicho. Usá algún emoji estratégico.",
  "caption_tiktok": "Caption para TikTok. Más corto, máximo 150 caracteres. Con 5 hashtags trending de música argentina.",
  "titulo_youtube": "Título para YouTube Shorts. Máximo 60 caracteres. Que genere curiosidad o urgencia.",
  "descripcion_youtube": "Descripción para YouTube Shorts. 2-3 líneas + hashtags."
}}"""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )

    respuesta_texto = message.content[0].text.strip()

    # Limpiar posibles markdown fences
    respuesta_texto = respuesta_texto.replace("```json", "").replace("```", "").strip()

    contenido = json.loads(respuesta_texto)
    contenido["titulo_noticia"] = noticia["titulo"]
    contenido["fuente"] = noticia["fuente"]  # no mostrar fuente
    contenido["fuente"] = noticia["fuente"]

    return contenido


def generar_lote(noticias: list, detalles: dict = {}) -> list:
    """Genera contenido para una lista de noticias"""
    resultados = []
    for i, noticia in enumerate(noticias):
        print(f"  ✍️  Generando contenido para: {noticia['titulo'][:50]}...")
        try:
            detalle = detalles.get(noticia["url"], "")
            contenido = generar_contenido(noticia, detalle)
            resultados.append(contenido)
            print(f"  ✅ Listo ({i+1}/{len(noticias)})")
        except Exception as e:
            print(f"  ❌ Error generando contenido: {e}")
    return resultados
