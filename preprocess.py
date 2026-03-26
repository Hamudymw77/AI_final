import os
import cv2

# --- NASTAVENÍ ---
VELIKOST_OBLICEJE = (128, 128) # Jednotná velikost pro neuronovou síť (Škálování)
VSTUPNI_SLOZKA = 'dataset'
VYSTUPNI_SLOZKA = 'dataset_cleaned'

# Načteme předtrénovaný detektor obličejů, který je zabudovaný přímo v OpenCV
# (Tohle není náš hlavní AI model, to je jen nástroj na přípravu dat)
detektor_obliceju = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def zpracuj_dataset():
    # Vytvoříme hlavní čistou složku, pokud neexistuje
    os.makedirs(VYSTUPNI_SLOZKA, exist_ok=True)
    
    kategorie = ['ronaldo', 'ostatni']
    
    for kat in kategorie:
        print(f"\nČistím a ořezávám kategorii: {kat}...")
        vstupni_cesta_kat = os.path.join(VSTUPNI_SLOZKA, kat)
        vystupni_cesta_kat = os.path.join(VYSTUPNI_SLOZKA, kat)
        
        # Vytvoříme podsložku v čistém datasetu (např. dataset_cleaned/ronaldo)
        os.makedirs(vystupni_cesta_kat, exist_ok=True)
        
        zpracovano = 0
        zahozeno = 0
        
        # Projdeme všechny stažené složky a podsložky
        for koren, _, soubory in os.walk(vstupni_cesta_kat):
            for nazev in soubory:
                if nazev.endswith((".jpg", ".jpeg", ".png")):
                    plna_cesta = os.path.join(koren, nazev)
                    
                    # 1. Načtení obrázku
                    obrazek = cv2.imread(plna_cesta)
                    if obrazek is None:
                        zahozeno += 1
                        continue
                    
                    # Pro detekci obličeje je lepší převést obrázek do černobílé
                    cernobily = cv2.cvtColor(obrazek, cv2.COLOR_BGR2GRAY)
                    
                    # 2. Detekce obličejů
                    obliceje = detektor_obliceju.detectMultiScale(cernobily, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))
                    
                    # 3. Čištění: Pokud na fotce není přesně 1 obličej, fotku zahodíme
                    # (Nechceme fotky bez lidí, ani fotky s 5 lidmi, kde nevíme, kdo je Ronaldo)
                    if len(obliceje) != 1:
                        zahozeno += 1
                        continue
                    
                    # 4. Transformace a Škálování
                    (x, y, w, h) = obliceje[0] # Vezmeme souřadnice nalezeného obličeje
                    
                    # Ořízneme obrázek jen na obličej (Crop)
                    vyriznuty_oblicej = obrazek[y:y+h, x:x+w]
                    
                    # Změníme velikost přesně na 128x128 pixelů (Resize)
                    vyriznuty_oblicej = cv2.resize(vyriznuty_oblicej, VELIKOST_OBLICEJE)
                    
                    # 5. Uložení vyčištěného obrázku
                    novy_nazev = f"{kat}_{zpracovano}.jpg"
                    nova_cesta = os.path.join(vystupni_cesta_kat, novy_nazev)
                    cv2.imwrite(nova_cesta, vyriznuty_oblicej)
                    
                    zpracovano += 1

        print(f" -> Úspěšně zpracováno a oříznuto: {zpracovano} fotek.")
        print(f" -> Zahozeno (špatné fotky/více lidí): {zahozeno} fotek.")

if __name__ == "__main__":
    zpracuj_dataset()