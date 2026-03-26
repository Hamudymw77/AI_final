
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
            
            # 2. Úprava barev a velikosti
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = cv2.resize(img, (128, 128))
            
            # 3. Normalizace (zkusíme ji nechat, uvidíme co vypíše terminal)
            img_array = img.astype('float32') / 255.0
            img_array = np.expand_dims(img_array, axis=0)
            
            # 4. PREDIKCE - TADY SE DĚJE MAGIE
            prediction = model.predict(img_array)[0][0]
            
            # TOTO JE KLÍČOVÉ: Podívej se do černého okna, co to vypíše!
            print(f">>> MODEL SI MYSLÍ ČÍSLO: {prediction}")

            # 5. ROZHODOVACÍ LOGIKA (Upravíme podle výsledku v terminálu)
            if prediction > 0.5:
                procenta = round(prediction * 100, 2)
                vysledek = f"Tohle JE Ronaldo! (Skóre: {procenta})"
            else:
                procenta = round((1 - prediction) * 100, 2)
                vysledek = f"Tohle NENÍ Ronaldo. (Skóre: {procenta})"

    return render_template('index.html', vysledek=vysledek)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)