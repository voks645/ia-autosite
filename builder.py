import os
import re
import requests
import openai
from datetime import datetime
from dotenv import load_dotenv

# Charger la clé OpenAI
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Créer les dossiers de site si nécessaire
os.makedirs("site/articles", exist_ok=True)

# Fonction pour obtenir un sujet tendance via l'IA
def get_trending_topic():
    prompt = (
        "Donne-moi un sujet d'actualité ou une tendance populaire actuelle qui pourrait faire un bon article de blog viral. Juste le titre du sujet."
    )
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=30
    )
    return response.choices[0].message.content.strip()

# Fonction pour obtenir une URL d'image résolue depuis Unsplash
def get_image_url(query="technologie"):
    response = requests.get(f"https://source.unsplash.com/800x600/?{query.replace(' ', '+')}")
    return response.url

# Fonction pour générer un article avec OpenAI
def generate_article(topic):
    prompt = (
        f"Rédige un article de blog sur le sujet suivant : '{topic}'. L'article doit être clair, structuré, avec une introduction, un développement, une conclusion, et optimisé pour le SEO."
    )
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=800
    )
    return response.choices[0].message.content

# Fonction pour sauvegarder l'article en HTML
def save_article_html(title, content, image_url):
    filename = re.sub(r"[^a-z0-9\-]", "", title.lower().replace(" ", "-"))[:50]
    date_str = datetime.now().strftime("%Y-%m-%d")
    filepath = f"site/articles/{filename}.html"

    converted_content = content.replace('\n', '</p><p>')

    article_html = f"""
    <html>
    <head>
        <meta charset='utf-8'>
        <title>{title}</title>
        <link href='https://fonts.googleapis.com/css2?family=Inter&display=swap' rel='stylesheet'>
        <link rel=\"stylesheet\" href=\"../style.css\">
    </head>
    <body>
        <header>
            <div class='header-content'>
                <h2><a href='../index.html'>🧠 Mon Site IA</a></h2>
            </div>
        </header>
        <div class='container'>
            <h1>{title}</h1>
            <p class='date'>{date_str}</p>
            <img src='{image_url}' alt='{title}' class='main-image'>
            <div class='content'>
                <p>{converted_content}</p>
            </div>
        </div>
        <footer>
            <p>Généré automatiquement par une IA &mdash; {date_str}</p>
        </footer>
    </body>
    </html>
    """

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(article_html)

    return filename + ".html"

# Fonction pour mettre à jour la page d'accueil
def update_index(title, article_filename):
    index_path = "site/index.html"
    date_str = datetime.now().strftime("%d %B %Y")
    link_html = f"<li><a href='articles/{article_filename}'>{title}</a> <span class='date'>({date_str})</span></li>\n"

    if not os.path.exists(index_path):
        with open(index_path, "w", encoding="utf-8") as f:
            f.write("""
            <html>
            <head>
                <meta charset='utf-8'>
                <title>Mon Site IA</title>
                <link href='https://fonts.googleapis.com/css2?family=Inter&display=swap' rel='stylesheet'>
                <link rel=\"stylesheet\" href=\"style.css\">
            </head>
            <body>
                <header>
                    <div class='header-content'>
                        <h2>🧠 Mon Site IA</h2>
                    </div>
                </header>
                <div class='container'>
                    <h1>Articles Récents</h1>
                    <ul id='articles-list'>
            """)

    with open(index_path, "a", encoding="utf-8") as f:
        f.write(link_html)

    if "</ul>" not in open(index_path, "r", encoding="utf-8").read():
        with open(index_path, "a", encoding="utf-8") as f:
            f.write("""
                    </ul>
                </div>
                <footer>
                    <p>Généré automatiquement par une IA.</p>
                </footer>
            </body>
            </html>
            """)

# Feuille de style modernisée et épurée
style_css = """
body {
    font-family: 'Inter', sans-serif;
    background: #f9fafb;
    color: #2d2d2d;
    margin: 0;
    padding: 0;
}
header {
    background: #0073e6;
    color: white;
    padding: 1rem;
    text-align: center;
}
.header-content h2 {
    margin: 0;
    font-size: 1.4rem;
}
.container {
    max-width: 800px;
    margin: 2rem auto;
    background: #fff;
    padding: 30px;
    border-radius: 10px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}
h1 {
    font-size: 2.2em;
    color: #333;
    margin-bottom: 10px;
}
.main-image {
    width: 100%;
    max-height: 400px;
    object-fit: cover;
    border-radius: 10px;
    margin: 1rem 0;
}
.date {
    font-size: 0.9em;
    color: #777;
    margin-bottom: 1rem;
}
.content p {
    line-height: 1.7;
    margin: 0 0 1em;
}
li {
    margin-bottom: 10px;
}
a {
    text-decoration: none;
    color: #0073e6;
}
a:hover {
    text-decoration: underline;
}
footer {
    text-align: center;
    font-size: 0.8em;
    color: #888;
    margin: 2rem 0;
}
"""
with open("site/style.css", "w", encoding="utf-8") as f:
    f.write(style_css)

# --- Execution ---
topic = get_trending_topic()
title = topic.title()
content = generate_article(topic)
image_url = get_image_url(topic)
filename = save_article_html(title, content, image_url)
update_index(title, filename)
print(f"✅ Article publié : site/articles/{filename}")