import requests
from bs4 import BeautifulSoup
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def scrape_la_viola():
    noticias = []
    try:
        url = "https://www.laviola.com.ar/"
        response = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        articulos = soup.find_all("article", limit=5)
        if not articulos:
            articulos = soup.find_all("div", class_=re.compile(r"post|article|noticia"), limit=5)
        for art in articulos:
            titulo_tag = art.find(["h1", "h2", "h3", "h4"])
            link_tag = art.find("a", href=True)
            if titulo_tag and link_tag:
                titulo = titulo_tag.get_text(strip=True)
                link = link_tag["href"]
                if not link.startswith("http"):
                    link = "https://www.laviola.com.ar" + link
                if titulo and len(titulo) > 15:
                    noticias.append({"titulo": titulo, "url": link, "fuente": "La Viola"})
    except Exception as e:
        print(f"Error scrapeando La Viola: {e}")
    return noticias


def scrape_rolling_stone_ar():
    noticias = []
    try:
        url = "https://www.rollingstone.com.ar/musica/"
        response = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        articulos = soup.find_all("article", limit=5)
        if not articulos:
            articulos = soup.find_all("div", class_=re.compile(r"post|card|item"), limit=5)
        for art in articulos:
            titulo_tag = art.find(["h1", "h2", "h3"])
            link_tag = art.find("a", href=True)
            if titulo_tag and link_tag:
                titulo = titulo_tag.get_text(strip=True)
                link = link_tag["href"]
                if not link.startswith("http"):
                    link = "https://www.rollingstone.com.ar" + link
                if titulo and len(titulo) > 15:
                    noticias.append({"titulo": titulo, "url": link, "fuente": "Rolling Stone AR"})
    except Exception as e:
        print(f"Error scrapeando Rolling Stone AR: {e}")
    return noticias


def scrape_infobae_cultura():
    noticias = []
    try:
        url = "https://www.infobae.com/cultura/"
        response = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        articulos = soup.find_all("article", limit=10)
        keywords = ["música", "musica", "rock", "trap", "canción", "cancion",
                    "disco", "artista", "banda", "concierto", "show", "festival",
                    "tour", "recital", "cantante", "álbum", "album", "reggaeton",
                    "cumbia", "folklore", "folclore", "pop", "metal", "punk"]
        for art in articulos:
            titulo_tag = art.find(["h1", "h2", "h3"])
            link_tag = art.find("a", href=True)
            if titulo_tag and link_tag:
                titulo = titulo_tag.get_text(strip=True)
                link = link_tag["href"]
                if not link.startswith("http"):
                    link = "https://www.infobae.com" + link
                if any(k in titulo.lower() for k in keywords) and len(titulo) > 15:
                    noticias.append({"titulo": titulo, "url": link, "fuente": "Infobae Cultura"})
    except Exception as e:
        print(f"Error scrapeando Infobae: {e}")
    return noticias


def obtener_detalle_noticia(url):
    """Obtiene el primer párrafo de la noticia para darle contexto a Claude"""
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        parrafos = soup.find_all("p", limit=6)
        texto = " ".join([p.get_text(strip=True) for p in parrafos if len(p.get_text(strip=True)) > 50])
        return texto[:800] if texto else ""
    except:
        return ""


def scrape_todas_las_fuentes():
    print("🔍 Scrapeando fuentes de noticias...")
    todas = []

    viola = scrape_la_viola()
    print(f"  La Viola: {len(viola)} noticias")
    todas.extend(viola)

    rolling = scrape_rolling_stone_ar()
    print(f"  Rolling Stone AR: {len(rolling)} noticias")
    todas.extend(rolling)

    infobae = scrape_infobae_cultura()
    print(f"  Infobae Cultura: {len(infobae)} noticias")
    todas.extend(infobae)

    # Eliminar duplicados por título similar
    vistos = set()
    unicas = []
    for n in todas:
        titulo_corto = n["titulo"][:40].lower()
        if titulo_corto not in vistos:
            vistos.add(titulo_corto)
            unicas.append(n)

    print(f"✅ Total noticias únicas encontradas: {len(unicas)}")
    return unicas[:6]  # Máximo 6 noticias por corrida
