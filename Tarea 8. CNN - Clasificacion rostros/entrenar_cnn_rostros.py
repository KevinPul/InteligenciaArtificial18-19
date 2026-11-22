import os
import json
import cv2
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from keras import layers, models


class EntrenadorCNN:
    def __init__(self, ruta_dataset, ruta_salida, img_size=64):
        self.ruta_dataset = ruta_dataset
        self.ruta_salida = ruta_salida
        self.img_size = img_size

        self.ruta_modelo = os.path.join(ruta_salida, 'modelo_cnn_rostros.keras')
        self.ruta_etiquetas = os.path.join(ruta_salida, 'etiquetas_rostros.json')

        self.detector_rostros = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )

        self.class_names = []
        self.train_images = None
        self.train_labels = None
        self.test_images = None
        self.test_labels = None
        self.model = None

    def recortar_rostro(self, img_bgr):
        gris = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        rostros = self.detector_rostros.detectMultiScale(
            gris, scaleFactor=1.2, minNeighbors=5, minSize=(60, 60)
        )

        if len(rostros) == 0:
            return None

        # Toma el rostro más grande detectado
        x, y, w, h = max(rostros, key=lambda r: r[2] * r[3])
        rostro_bgr = img_bgr[y:y+h, x:x+w]

        # Convierte el rostro a RGB y lo redimensiona
        rostro_rgb = cv2.cvtColor(rostro_bgr, cv2.COLOR_BGR2RGB)
        return cv2.resize(rostro_rgb, (self.img_size, self.img_size))

    def cargar_dataset(self):
        self.class_names = sorted([
            carpeta for carpeta in os.listdir(self.ruta_dataset)
            if os.path.isdir(os.path.join(self.ruta_dataset, carpeta))
        ])
        print("Clases detectadas:", self.class_names)

        imagenes = []
        etiquetas = []

        for idx, nombre in enumerate(self.class_names):
            carpeta_persona = os.path.join(self.ruta_dataset, nombre)
            contador = 0

            for archivo in sorted(os.listdir(carpeta_persona)):
                ruta_img = os.path.join(carpeta_persona, archivo)
                datos = np.fromfile(ruta_img, dtype=np.uint8)
                img_bgr = cv2.imdecode(datos, cv2.IMREAD_COLOR)
                if img_bgr is None:
                    continue
                # Solo le interesa el rostro para entrenamiento
                rostro = self.recortar_rostro(img_bgr)
                if rostro is not None:
                    imagenes.append(rostro)
                    etiquetas.append(idx)
                    contador += 1

            print(f"  {nombre}: {contador} rostros válidos")

        imagenes = np.array(imagenes)
        etiquetas = np.array(etiquetas)

        # Mezcla aleatoriamente y divide 80% entrenamiento / 20% prueba
        indices = np.random.permutation(len(imagenes))
        imagenes = imagenes[indices]
        etiquetas = etiquetas[indices]

        corte = int(len(imagenes) * 0.8)
        self.train_images, self.test_images = imagenes[:corte], imagenes[corte:]
        self.train_labels, self.test_labels = etiquetas[:corte], etiquetas[corte:]

        # Valores entre 0 y 1
        self.train_images = self.train_images / 255.0
        self.test_images = self.test_images / 255.0

        print(f"Entrenamiento: {len(self.train_images)} | Prueba: {len(self.test_images)}")

    def verificar_datos(self):
        plt.figure(figsize=(10, 10))
        for i in range(min(25, len(self.train_images))):
            plt.subplot(5, 5, i + 1)
            plt.xticks([])
            plt.yticks([])
            plt.grid(False)
            plt.imshow(self.train_images[i])
            plt.xlabel(self.class_names[self.train_labels[i]])
        plt.show()

    def construir_modelo(self):
        # Arquitectura de la CNN
        self.model = models.Sequential()
        self.model.add(layers.Conv2D(32, (3, 3), activation='relu',
                                     input_shape=(self.img_size, self.img_size, 3)))
        self.model.add(layers.MaxPooling2D((2, 2)))
        self.model.add(layers.Conv2D(64, (3, 3), activation='relu'))
        self.model.add(layers.MaxPooling2D((2, 2)))
        self.model.add(layers.Conv2D(64, (3, 3), activation='relu'))

        self.model.add(layers.Flatten())
        self.model.add(layers.Dense(64, activation='relu'))
        self.model.add(layers.Dense(len(self.class_names)))

        self.model.summary()

    def entrenar_y_evaluar(self, epochs=15):
        self.model.compile(
            optimizer='adam',
            loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
            metrics=['accuracy']
        )

        history = self.model.fit(
            self.train_images, self.train_labels,
            epochs=epochs,
            validation_data=(self.test_images, self.test_labels)
        )

        test_loss, test_acc = self.model.evaluate(self.test_images, self.test_labels, verbose=2)
        print("Precisión en prueba:", test_acc)
        print("Error calculado:", test_loss)

        # Gráfica de precisión
        plt.plot(history.history['accuracy'], label='accuracy')
        plt.plot(history.history['val_accuracy'], label='val_accuracy')
        plt.text(0.5, 0.88, f"accuracy: {test_acc:.8f} %\nerror: {test_loss:.8f}", fontsize=10)
        plt.ylim([0, 1])
        plt.xlabel('Epoch')
        plt.ylabel('Accuracy')
        plt.legend(loc='lower right')
        plt.show()


        # Guardar modelo entrenado y etiquetas del dataset
        self.model.save(self.ruta_modelo)
        with open(self.ruta_etiquetas, 'w', encoding='utf-8') as f:
            json.dump(self.class_names, f, ensure_ascii=False, indent=4)

        print("Modelo guardado en:", self.ruta_modelo)

# Main para entrenamiento
if __name__ == "__main__":
    ruta_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_dataset = os.path.join(
        os.path.dirname(ruta_actual),
        'Tarea 6. Crear Dataset Propio',
        'Dataset_Famosos'
    )

    entrenador = EntrenadorCNN(
        ruta_dataset=ruta_dataset,
        ruta_salida=ruta_actual,
        img_size=64
    )
    entrenador.cargar_dataset()
    entrenador.verificar_datos()
    entrenador.construir_modelo()
    entrenador.entrenar_y_evaluar(epochs=15)