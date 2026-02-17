import requests
from bs4 import BeautifulSoup
import csv

# 1. Liste des écoles à surveiller (Exemples fictifs)
ecoles = [
    {"nom": "Ecole de Voile A", "url": "https://www.ecole-exemple-a.com/catamaran"},
    {"nom": "Cata-Club B", "url": "https://www.cata-club-b.fr/tarifs"},
]

def extraire_donnees(ecole):
    try:
        # Le robot visite le site
        response = requests.get(ecole['url'], timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        # --- C'EST ICI QU'ON ADAPTE SELON CHAQUE SITE ---
        # On cherche le prix, le lieu et la taille dans le code HTML
        # Ces sélecteurs (class_) sont des exemples, ils changent selon le site.
        prix = soup.find(class_="price").text.strip() if soup.find(class_="price") else "N/A"
        lieu = soup.find(class_="location").text.strip() if soup.find(class_="location") else "Bretagne"
        taille = "40 pieds" # Souvent fixe par page, ou à chercher dans le titre
        # -----------------------------------------------

        return [ecole['nom'] + " (" + taille + ")", lieu, prix, ecole['url']]
    except Exception as e:
        print(f"Erreur sur {ecole['nom']}: {e}")
        return None

# 2. Exécution et création du fichier CSV
resultats = []
for ecole in ecoles:
    data = extraire_donnees(ecole)
    if data:
        resultats.append(data)

# 3. On enregistre le fichier que WordPress va lire
with open('tarifs.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    # Entêtes des colonnes
    writer.writerow(['Bateau', 'Lieu', 'Prix', 'Lien'])
    writer.writerows(resultats)

print("Robot a fini sa mission : tarifs.csv mis à jour.")
