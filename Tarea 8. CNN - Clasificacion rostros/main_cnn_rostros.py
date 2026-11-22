import os
import json
import cv2
import numpy as np
import tensorflow as tf


class Main:
    def __init__(self):
        self.ruta_actual = os.path.dirname(os.path.abspath(__file__))
        self.ruta_modelo = os.path.join(self.ruta_actual, 'modelo_cnn_rostros.keras')
        self.ruta_etiquetas = os.path.join(self.ruta_actual, 'etiquetas_rostros.json')
        self.img_size = 64

        self.detector_rostros = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )

    def transformar_rostro(self, rostro_bgr):
        # Convertir a RGB y redimensionar
        rostro_rgb = cv2.cvtColor(rostro_bgr, cv2.COLOR_BGR2RGB)
        return cv2.resize(rostro_rgb, (self.img_size, self.img_size))

    def reconocer_en_vivo(self):
        if not os.path.exists(self.ruta_modelo) or not os.path.exists(self.ruta_etiquetas):
            raise FileNotFoundError(
                "No se encontró el modelo entrenado. Ejecuta primero entrenar_cnn_rostros.py."
            )

        # Carga el modelo entrenado
        model = tf.keras.models.load_model(self.ruta_modelo)
        with open(self.ruta_etiquetas, 'r', encoding='utf-8') as f:
            class_names = json.load(f)

        # Activa camara para capturar video
        camara = cv2.VideoCapture(0)
        if not camara.isOpened():
            raise RuntimeError("No se pudo abrir la cámara web.")

        nombre_ventana = "CNN - Clasificacion Rostros en Tiempo Real"
        print("Cierra la ventana (X) para salir.")

        while True:
            ret, fotograma = camara.read()
            if not ret:
                break
            # Metodo para detectar rostros
            gris = cv2.cvtColor(fotograma, cv2.COLOR_BGR2GRAY)
            rostros = self.detector_rostros.detectMultiScale(
                gris,
                scaleFactor=1.2,
                minNeighbors=5,
                minSize=(80, 80)
            )

            for (x, y, w, h) in rostros:
                rostro_bgr = fotograma[y:y+h, x:x+w]
                rostro_prep = self.transformar_rostro(rostro_bgr)

                # Normalizar entre 0 y 1
                entrada = rostro_prep / 255.0
                entrada = np.expand_dims(entrada, axis=0)

                # Convertir a probabilidades
                logits = model.predict(entrada, verbose=0)
                probabilidades = tf.nn.softmax(logits[0]).numpy()

                indice = int(np.argmax(probabilidades))
                confianza = float(np.max(probabilidades)) * 100
                # Si la confianza es mayor o igual a 85% dice el nombre, de lo contrario desconocido
                if confianza >= 85.0:
                    nombre = class_names[indice]
                    color = (0, 255, 0)
                else:
                    nombre = "Desconocido"
                    color = (0, 0, 255)

                texto = f"{nombre}: {confianza:.1f}%"
                # Pone la prediccion del modelo
                cv2.rectangle(fotograma, (x, y), (x+w, y+h), color, 2)
                cv2.putText(
                    fotograma, texto, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2
                )

            cv2.imshow(nombre_ventana, fotograma)
            cv2.waitKey(1)
            
            # Cerrar ventana
            if cv2.getWindowProperty(nombre_ventana, cv2.WND_PROP_VISIBLE) < 1:
                break

        camara.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    app = Main()
    app.reconocer_en_vivo()