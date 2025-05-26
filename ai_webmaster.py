import os
import subprocess
import datetime

# Nom du dossier du site
SITE_DIR = "site"

# Vérifie si l'article d'aujourd'hui existe déjà
def already_published_today():
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    articles_path = os.path.join(SITE_DIR, "articles")
    if not os.path.exists(articles_path):
        return False
    for filename in os.listdir(articles_path):
        if filename.startswith(today):
            return True
    return False

# Exécute builder.py pour générer un nouvel article
def generate_article():
    print("🧠 Génération de l'article avec l'IA...")
    subprocess.run([os.sys.executable, "builder.py"], check=True)

# Push les fichiers sur GitHub Pages
def deploy_to_github():
    print("🚀 Déploiement sur GitHub Pages...")
    subprocess.run(["git", "add", "site"], check=True)
    subprocess.run(["git", "commit", "-m", "Ajout article IA du jour"], check=True)
    subprocess.run(["git", "push"], check=True)

if __name__ == "__main__":
    if already_published_today():
        print("✅ Un article a déjà été publié aujourd'hui.")
    else:
        generate_article()
        deploy_to_github()
        print("🌍 Site mis à jour avec un nouvel article IA.")