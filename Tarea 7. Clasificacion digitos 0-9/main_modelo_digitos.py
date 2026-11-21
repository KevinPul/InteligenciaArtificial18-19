import os
import tkinter as tk
import numpy as np
import tensorflow as tf
from PIL import Image, ImageDraw

# Carga el modelo del keras
ruta_carpeta = os.path.dirname(os.path.abspath(__file__))
ruta_modelo = os.path.join(ruta_carpeta, 'modelo_mnist.keras')
model = tf.keras.models.load_model(ruta_modelo)

gray_scale = 255
ultimo_x, ultimo_y = None, None

# Crea lienzo y ventana
ventana = tk.Tk()
ventana.title("Clasificación Dígitos 0-9")

canvas = tk.Canvas(ventana, width=280, height=280, bg='black')
canvas.pack(pady=10, padx=10)

# Copia del dibujo en escala de grises
imagen = Image.new("L", (280, 280), 0)
dibujo = ImageDraw.Draw(imagen)

lbl_resultado = tk.Label(ventana, text="Dibuja un dígito (0-9)", font=("Arial", 16, "bold"))
lbl_resultado.pack(pady=5)

def iniciar_trazo(evento):
    global ultimo_x, ultimo_y
    ultimo_x, ultimo_y = evento.x, evento.y

def dibujar(evento):
    global ultimo_x, ultimo_y
    x, y = evento.x, evento.y
    grosor = 14

    if ultimo_x is not None and ultimo_y is not None:
        canvas.create_line(ultimo_x, ultimo_y, x, y, fill='white', width=grosor, capstyle=tk.ROUND)
        dibujo.line([ultimo_x, ultimo_y, x, y], fill=255, width=grosor)

    ultimo_x, ultimo_y = x, y
    predecir()

def predecir():
    # Recorta del lienzo lo que no se use
    caja = imagen.getbbox()
    if caja is None:
        return
    recorte = imagen.crop(caja)

    # Redimensiona la imagen en 20x20 proporcionalmente
    ancho, alto = recorte.size
    escala = 20 / max(ancho, alto)
    nuevo_ancho = max(1, int(ancho * escala))
    nuevo_alto = max(1, int(alto * escala))
    numero_20 = recorte.resize((nuevo_ancho, nuevo_alto))

    # Crea un lienzo en blanco de 28x28
    lienzo_28 = Image.new("L", (28, 28), 0)

    # Calcula el punto de la esquina superior izquierda para quedar centrado
    x_centro = (28 - nuevo_ancho) // 2
    y_centro = (28 - nuevo_alto) // 2

    # Pega el numero 20x20 en el centro del lienzo 28x28
    lienzo_28.paste(numero_20, (x_centro, y_centro))

    # Normaliza los datos para que sean de 0 a 1
    entrada = np.array(lienzo_28).astype('float32') / gray_scale
    entrada = entrada.reshape(1, 28, 28)

    # Predice con la red neuronal
    prediccion = model.predict(entrada, verbose=0)
    digito = np.argmax(prediccion)
    confianza = np.max(prediccion) * 100
    lbl_resultado.config(text=f"Predicción: {digito} ({confianza:.1f}%)")

# Limpia el canva
def limpiar():
    global ultimo_x, ultimo_y
    ultimo_x, ultimo_y = None, None
    canvas.delete("all")
    dibujo.rectangle([0, 0, 280, 280], fill=0)
    lbl_resultado.config(text="Dibuja un dígito (0-9)")

btn_limpiar = tk.Button(ventana, text="Limpiar", command=limpiar, font=("Arial", 12))
btn_limpiar.pack(pady=5)

canvas.bind("<Button-1>", iniciar_trazo)
canvas.bind("<B1-Motion>", dibujar)
ventana.mainloop()