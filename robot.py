import requests
from bs4 import BeautifulSoup
import csv
import re
import time

# --- LA LISTE DES CIBLES (Leaders Mondiaux & Écoles) ---
urls_cibles = [
    {"nom": "Sunsail", "url": "https://www.sunsail.fr/location-bateaux/catamarans"},
    {"nom": "Dream Yacht", "url": "https://www.dreamyachtcharter.fr/croisiere-a-la-cabine/"},
    {"nom": "Moorings", "url": "https://www.moorings.fr/location-catamaran"},
    {"nom": "Les Glénans", "url": "https://www.glenans.asso.fr/recherche-stage?discipline=Croisi%C3%A8re&bateau=Catamaran"},
    {"nom": "UCPA", "url": "https://www.ucpa.com/croisiere-voile/catamaran"},
    {"nom": "Macif Centre Voile", "url": "https://www.macifcentredevoile.com/rechercher-un-stage?type_bateau=catamaran"},
    {"nom": "GlobeSailor", "url": "https://www.globesailor.fr/croisiere-cabine-catamaran-c1.html"},
    {"nom": "Skippair", "url": "https://www.skippair.com/fr/croisiere-voile/catamaran/"},
    {"nom": "VogFleet", "url": "https://www.vogfleet.com/fr/croisiere-catamaran"},
    {"nom": "Spi en Ligne", "url": "https://www.spi-en-ligne.com/stages-de-voile-catamaran/"},
    {"nom": "Click&Boat", "url": "https://www.clickandboat.com/location-catamaran"},
    {"nom": "Samboat", "url": "https://www.samboat.fr/location-bateau/catamaran"}
]

def extraire_donnees_avancees(ecole):
    print(f"Analyse de {ecole['nom']}...")
    try:
        # On simule un vrai navigateur (User-Agent) pour éviter les blocages
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7'
        }
        
        response = requests.get(ecole['url'], headers=headers, timeout=20)
        soup = BeautifulSoup(response.text, 'html.parser')
        page_text = soup.get_text()

        # 1. Recherche du PRIX (Cherche un nombre suivi de € ou EUR)
        # On prend le premier prix significatif trouvé (souvent le "à partir de")
        prix_matches = re.findall(r'(\d{3,4})\s?(?:€|EUR)', page_text)
        prix = prix_matches[0] if prix_matches else "Voir site"

        # 2. Recherche de la TAILLE (Cherche 38-50 suivi de ft, pieds ou m)
        taille_matches = re.findall(r'(\d{2})\s?(?:ft|pieds|m)', page_text)
        taille = taille_matches[0] + " ft" if taille_matches else "40+ ft"

        # 3. Recherche du LIEU
        lieux_possibles = ["Antilles", "Bretagne", "Méditerranée", "Corse", "Croatie", "Grèce", "Seychelles"]
        lieu = "International"
        for l in lieux_possibles:
            if l.lower() in page_text.lower():
                lieu = l
                break

        return [ecole['nom'], taille, lieu, prix, ecole['url']]

    except Exception as e:
        print(f"Erreur sur {ecole['nom']}: {e}")
        return [ecole['nom'], "N/A", "N/A", "Erreur", ecole['url']]

# --- EXECUTION ---
resultats = []
for ecole in urls_cibles:
    data = extraire_donnees_avancees(ecole)
    resultats.append(data)
    time.sleep(2) # Pause de 2 sec pour ne pas être banni

# --- SAUVEGARDE CSV ---
with open('tarifs.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Ecole/Charter', 'Taille Bateau', 'Lieu Principal', 'Prix (à partir de)', 'Lien'])
    writer.writerows(resultats)

print("\n--- Mission terminée : tarifs.csv généré avec succès ---")
