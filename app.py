import os
import cv2
import numpy as np
from flask import Flask, request, render_template
from tensorflow.keras.models import load_model

app = Flask(__name__)

# Načtení modelu
MODEL_PATH = 'ronaldo_model.h5'
try:
    model = load_model(MODEL_PATH)
    print("--- MODEL JE PŘIPRAVEN ---")
except Exception as e:
    print(f"CHYBA: {e}")

# Načtení detektoru obličejů
detektor = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

@app.route('/', methods=['GET', 'POST'])
def index():
    vysledek = None
    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            # 1. Načtení fotky
            filestr = file.read()
            npimg = np.frombuffer(filestr, np.uint8)
            img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

            # 2. Úprava barev (BGR na RGB)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # 3. Detekce obličeje
            cernobily = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            obliceje = detektor.detectMultiScale(cernobily, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))

            if len(obliceje) == 0:
                vysledek = "Na fotce nebyl nalezen žádný obličej."
                return render_template('index.html', vysledek=vysledek)

            # Vezme první nalezený obličej a ořízne ho
            (x, y, w, h) = obliceje[0]
            img = img[y:y+h, x:x+w]

            # 4. Resize a normalizace
            img = cv2.resize(img, (128, 128))
            img_array = img.astype('float32')
            img_array = np.expand_dims(img_array, axis=0)

            # 5. Predikce
            surova_predikce = model.predict(img_array)[0]
            print(f">>> VŠECHNA ČÍSLA Z MODELU: {surova_predikce}")

            # 6. Univerzální rozhodovací logika
            # Zjistíme, jestli model vrací pole dvou čísel (Softmax) nebo jedno číslo (Sigmoid)
            if len(surova_predikce) > 1:
                pravdepodobnost_ronaldo = surova_predikce[1]
                pravdepodobnost_ostatni = surova_predikce[0]
            else:
                pravdepodobnost_ronaldo = surova_predikce[0]
                pravdepodobnost_ostatni = 1.0 - pravdepodobnost_ronaldo

            # Vyhodnocení (hranice 0.5)
            if pravdepodobnost_ronaldo > 0.5:
                procenta = round(float(pravdepodobnost_ronaldo) * 100, 2)
                vysledek = f"Tohle JE Ronaldo! (Skóre: {procenta}%)"
            else:
                procenta = round(float(pravdepodobnost_ostatni) * 100, 2)
                vysledek = f"Tohle NENÍ Ronaldo. (Jistota modelu: {procenta}%)"

    return render_template('index.html', vysledek=vysledek)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
