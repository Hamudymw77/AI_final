import os
import csv
import cv2
from icrawler.builtin import BingImageCrawler

# --- 1. ČÁST: STAHOVÁNÍ OBRÁZKŮ (Doplňková verze pro dosažení 1500+) ---
def stahni_obrazky():
    # Nové dotazy pro Ronalda
    dotazy_ronaldo = [
        "Cristiano Ronaldo Portugal face", "Cristiano Ronaldo Sporting CP face", 
        "Cristiano Ronaldo 2020 face", "Cristiano Ronaldo laughing face", 
        "Cristiano Ronaldo training face", "Cristiano Ronaldo interview face", 
        "Cristiano Ronaldo 2022 face"
    ]
    
    # Nové dotazy pro ostatní lidi
    dotazy_ostatni = [
        "basketball player face", "tennis player face", "actor face close up", 
        "singer face close up", "news anchor face", "generic human face profile", 
        "rugby player face", "golf player face", "man face portrait photography"
    ]

    print("Dostahovávám chybějící data fotek Ronalda...")
    stahni_kategorii(dotazy_ronaldo, 'dataset/ronaldo', 150)

    print("Dostahovávám chybějící data fotek ostatních...")
    stahni_kategorii(dotazy_ostatni, 'dataset/ostatni', 150)

def stahni_kategorii(dotazy, hlavni_slozka, limit_na_dotaz):
    for dotaz in dotazy:
        print(f" ---> Hledám a stahuji: {dotaz}...")
        
        # Vytvoříme podsložku pro každý dotaz, aby se soubory nepřepisovaly
        specificka_slozka = os.path.join(hlavni_slozka, dotaz.replace(" ", "_"))
        os.makedirs(specificka_slozka, exist_ok=True)
        
        # Inicializace iCrawleru s cílovou složkou
        crawler = BingImageCrawler(storage={'root_dir': specificka_slozka})
        
        # Samotné spuštění stahování
        crawler.crawl(keyword=dotaz, max_num=limit_na_dotaz)

# --- 2. ČÁST: TVORBA CSV S ATRIBUTY (Předzpracování metadat) ---
def vytvor_csv():
    hlavicka = ["cesta_k_souboru", "sirka", "vyska", "prumerny_jas", "label"]

    with open("dataset_info.csv", mode="w", newline="", encoding="utf-8") as soubor:
        zapisovac = csv.writer(soubor)
        zapisovac.writerow(hlavicka)

        print("\nZpracovávám atributy pro Ronalda...")
        zpracuj_slozku('dataset/ronaldo', 1, zapisovac)

        print("Zpracovávám atributy pro ostatní...")
        zpracuj_slozku('dataset/ostatni', 0, zapisovac)

def zpracuj_slozku(cesta_slozky, label, zapisovac):
    if not os.path.exists(cesta_slozky):
        return

    # os.walk bez problémů projde i všechny podsložky (staré i nové)
    for koren, podslozky, soubory in os.walk(cesta_slozky):
        for nazev_souboru in soubory:
            if nazev_souboru.endswith((".jpg", ".jpeg", ".png")):
                plna_cesta = os.path.join(koren, nazev_souboru)
                obrazek = cv2.imread(plna_cesta)

                # Přeskočíme poškozené soubory
                if obrazek is None:
                    continue

                vyska, sirka, _ = obrazek.shape
                prumerny_jas = obrazek.mean()

                zapisovac.writerow([plna_cesta, sirka, vyska, round(prumerny_jas, 2), label])

# --- SPUŠTĚNÍ PROGRAMU ---
if __name__ == "__main__":
    stahni_obrazky()
    vytvor_csv()
    print("\n Vše je hotovo! Data jsou připravena.")