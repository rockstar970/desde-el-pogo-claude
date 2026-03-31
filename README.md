# 🎸 Desde el Pogo — Generador Automático de Contenido

Scraper + generador de contenido para músic argentina usando Claude AI.
Corre automáticamente 2 veces por día y genera guiones + captions para Instagram, TikTok y YouTube Shorts.

## ¿Qué hace?

1. **Scrapea** noticias de La Viola, Rolling Stone AR e Infobae Cultura
2. **Genera** con Claude API: guion para video, caption Instagram, caption TikTok, título y descripción YouTube
3. **Guarda** el contenido en archivos JSON en la carpeta `output/`
4. **Corre solo** dos veces por día (9 AM y 6 PM hora Argentina)

---

## Setup local (para probar)

### 1. Clonar e instalar dependencias
```bash
git clone <tu-repo>
cd desde-el-pogo
pip install -r requirements.txt
```

### 2. Configurar credenciales
```bash
cp .env.example .env
# Editá .env y poné tu ANTHROPIC_API_KEY real
```

### 3. Correr
```bash
# Correr una vez (para probar)
python main.py

# Correr con scheduler automático
python scheduler.py
```

---

## Deploy en Railway

### 1. Subir a GitHub
```bash
git init
git add .
git commit -m "initial commit"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/desde-el-pogo.git
git push -u origin main
```

### 2. Crear proyecto en Railway
- Entrá a [railway.app](https://railway.app)
- New Project → Deploy from GitHub repo
- Seleccioná tu repo

### 3. Configurar variable de entorno en Railway
- En tu proyecto → Variables
- Agregar: `ANTHROPIC_API_KEY` = tu key real

### 4. Listo
Railway va a detectar el `Procfile` y correr `python scheduler.py` automáticamente.

---

## Estructura de archivos output

Cada corrida genera un archivo `output/contenido_YYYYMMDD_HHMMSS.json` con esta estructura:

```json
[
  {
    "titulo_noticia": "Título de la noticia scrapeada",
    "fuente": "La Viola",
    "url_fuente": "https://...",
    "guion_corto": "Guion de 30-45 segundos para el video...",
    "caption_instagram": "Caption con hashtags para Instagram...",
    "caption_tiktok": "Caption corto para TikTok...",
    "titulo_youtube": "Título para YouTube Shorts",
    "descripcion_youtube": "Descripción para YouTube Shorts..."
  }
]
```

---

## Próximos pasos (módulos futuros)

- [ ] Módulo de creación de video automático (moviepy + imágenes)
- [ ] Módulo de publicación en TikTok API
- [ ] Módulo de publicación en YouTube API
- [ ] Módulo de publicación en Instagram (Meta API)
