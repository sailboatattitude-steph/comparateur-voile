import requests
from bs4 import BeautifulSoup
import csv
import re

def scraper_professionnel():
    # Liste étendue (ajoute autant d'URLs que tu veux ici)
    urls = [
        {"n": "Sunsail", "u": "https://www.sunsail.fr/"},
        {"n": "Dream Yacht", "u": "https://www.dreamyachtcharter.fr/"},
        {"n": "Moorings", "u": "https://www.moorings.fr/"},
        {"n": "Glenans", "u": "https://www.glenans.asso.fr/"},
        {"n": "UCPA", "u": "https://www.ucpa.com/"},
        {"n": "GlobeSailor", "u": "https://www.globesailor.fr/"},
        {"n": "VogFleet", "u": "https://www.vogfleet.com/"},
        {"n": "Macif", "u": "https://www.macifcentredevoile.com/"}
    ]
    
    data_finale = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

    for item in urls:
        try:
            # On tente de récupérer la page
            r = requests.get(item['u'], headers=headers, timeout=5)
            # On extrait grossièrement un prix pour le test
            prix = re.findall(r'(\d{3,4})\s?€', r.text)
            p = prix[0] if prix else "A vérifier"
            data_finale.append([item['n'], "40-45ft", "Global", p, item['u']])
        except:
            # Si un site bloque (Sunsail par exemple), on n'arrête pas le robot !
            data_finale.append([item['n'], "N/A", "N/A", "Lien Direct", item['u']])

    # Écriture du fichier quoi qu'il arrive
    with open('tarifs.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Source', 'Taille', 'Lieu', 'Prix', 'URL'])
        writer.writerows(data_finale)

if __name__ == "__main__":
    scraper_professionnel()
