import json
import os
from datetime import datetime
from dotenv import load_dotenv

from scraper import scrape_todas_las_fuentes, obtener_detalle_noticia
from generator import generar_lote

load_dotenv()

def cargar_noticias_procesadas():
    """Carga las URLs ya procesadas para no repetir contenido"""
    try:
        with open("procesadas.json", "r", encoding="utf-8") as f:
            return set(json.load(f))
    except:
        return set()

def guardar_noticias_procesadas(urls: set):
    # Mantener solo las últimas 100 para no crecer infinito
    lista = list(urls)[-100:]
    with open("procesadas.json", "w", encoding="utf-8") as f:
        json.dump(lista, f)

def guardar_resultados(resultados: list):
    """Guarda el contenido generado en un archivo JSON con timestamp"""
    if not resultados:
        return
    os.makedirs("output", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"output/contenido_{timestamp}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)
    print(f"\n💾 Contenido guardado en: {filename}")
    return filename

def mostrar_preview(resultados: list):
    """Muestra un preview del contenido generado en consola"""
    print("\n" + "="*60)
    print("📱 PREVIEW DEL CONTENIDO GENERADO")
    print("="*60)
    for i, r in enumerate(resultados, 1):
        print(f"\n🎵 Noticia {i}: {r['titulo_noticia'][:55]}...")
        print(f"📰 Fuente: {r['fuente']}")
        print(f"\n🎬 GUION:\n{r['guion_corto']}")
        print(f"\n📸 INSTAGRAM:\n{r['caption_instagram']}")
        print(f"\n🎵 TIKTOK:\n{r['caption_tiktok']}")
        print(f"\n▶️  YOUTUBE TÍTULO: {r['titulo_youtube']}")
        print("-"*60)

def main():
    print("\n🎸 DESDE EL POGO — Generador de Contenido")
    print(f"🕐 Corriendo: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")

    # Verificar API key
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("❌ Error: ANTHROPIC_API_KEY no configurada en .env")
        return

    # 1. Scraping
    noticias = scrape_todas_las_fuentes()

    if not noticias:
        print("⚠️  No se encontraron noticias. Intentá de nuevo más tarde.")
        return

    # 2. Filtrar ya procesadas
    procesadas = cargar_noticias_procesadas()
    noticias_nuevas = [n for n in noticias if n["url"] not in procesadas]

    if not noticias_nuevas:
        print("ℹ️  Todas las noticias de hoy ya fueron procesadas.")
        return

    print(f"\n📰 Noticias nuevas a procesar: {len(noticias_nuevas)}")

    # 3. Obtener detalles de cada noticia
    print("\n🔎 Obteniendo detalles de cada noticia...")
    detalles = {}
    for n in noticias_nuevas:
        detalles[n["url"]] = obtener_detalle_noticia(n["url"])

    # 4. Generar contenido con Claude
    print("\n🤖 Generando contenido con Claude...")
    resultados = generar_lote(noticias_nuevas, detalles)

    if not resultados:
        print("❌ No se pudo generar contenido.")
        return

    # 5. Guardar resultados
    archivo = guardar_resultados(resultados)

    # 6. Marcar como procesadas
    nuevas_urls = {n["url"] for n in noticias_nuevas}
    guardar_noticias_procesadas(procesadas | nuevas_urls)

    # 7. Mostrar preview
    mostrar_preview(resultados)

    print(f"\n✅ ¡Listo! Se generó contenido para {len(resultados)} publicaciones.")
    print(f"📁 Encontralo en: {archivo}")

if __name__ == "__main__":
    main()
