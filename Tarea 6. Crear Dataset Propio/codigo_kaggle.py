import hashlib
import os
import shutil
import cv2
import kagglehub
import numpy as np

# Descargar dataset de kaggle
print("Verificando dataset principal...")
ruta_original = kagglehub.dataset_download("vishesh1412/celebrity-face-image-dataset")
carpeta_dataset = os.path.join(ruta_original, "Celebrity Faces Dataset")

# Famosos elegidos
famosos_elegidos = [
    "Angelina Jolie",
    "Brad Pitt",
    "Tom Cruise",
    "Scarlett Johansson",
    "Will Smith"
]
MAX_POR_CLASE = 100 # Maximo 100 imagenes por famoso

# Cargar detectores faciales
detector_frontal = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)
detector_alt = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_alt2.xml"
)
# Evalua si el rostro es valido para extraer (2 valido, 1 valido con angulo, 0 no valido)
def evaluar_rostro(img_bgr):
    gris = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    alto, ancho = gris.shape
    lado_min = max(50, int(min(ancho, alto) * 0.15))

    rostros = detector_frontal.detectMultiScale(
        gris, scaleFactor=1.1, minNeighbors=6, minSize=(lado_min, lado_min)
    )
    if len(rostros) > 0:
        return 2

    rostros = detector_frontal.detectMultiScale(
        gris, scaleFactor=1.1, minNeighbors=4, minSize=(lado_min, lado_min)
    )
    if len(rostros) == 0 and not detector_alt.empty():
        rostros = detector_alt.detectMultiScale(
            gris, scaleFactor=1.1, minNeighbors=4, minSize=(lado_min, lado_min)
        )
    return 1 if len(rostros) > 0 else 0

# Ruta de guardado
ruta_script = os.path.dirname(os.path.abspath(__file__))
carpeta_tarea = os.path.join(ruta_script, "Dataset_Famosos")
os.makedirs(carpeta_tarea, exist_ok=True)

# Filtrado y extraccion de imagenes validas
for famoso in famosos_elegidos:
    origen = os.path.join(carpeta_dataset, famoso)
    destino = os.path.join(carpeta_tarea, famoso)

    if not os.path.exists(origen):
        print(f"No se encontró a {famoso} en el dataset original.")
        continue

    if os.path.exists(destino):
        shutil.rmtree(destino)
    os.makedirs(destino, exist_ok=True)

    hashes_vistos = set()
    prioridad_alta = []   # Rostros frontales muy claros
    prioridad_media = []  # Rostros válidos con angulos

    for archivo in sorted(os.listdir(origen)):
        ruta_img = os.path.join(origen, archivo)
        if not os.path.isfile(ruta_img):
            continue
        # Leer bytes directamente
        datos = np.fromfile(ruta_img, dtype=np.uint8)
        img_bgr = cv2.imdecode(datos, cv2.IMREAD_COLOR)
        if img_bgr is None:
            continue
        # Deteccion de duplicados
        mini = cv2.resize(cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY), (16, 16))
        huella = hashlib.md5(mini.tobytes()).hexdigest()
        if huella in hashes_vistos:
            continue
        hashes_vistos.add(huella)

        calidad = evaluar_rostro(img_bgr)
        if calidad == 2:
            prioridad_alta.append(ruta_img)
        elif calidad == 1:
            prioridad_media.append(ruta_img)

    seleccionadas = (prioridad_alta + prioridad_media)[:MAX_POR_CLASE]

    for idx, ruta_src in enumerate(seleccionadas, start=1):
        ext = os.path.splitext(ruta_src)[1].lower() or ".jpg"
        ruta_dst = os.path.join(destino, f"{idx:03d}{ext}")
        shutil.copy2(ruta_src, ruta_dst)

    print(f"{famoso}: {len(seleccionadas)} imágenes únicas copiadas (frontales estrictas: {len(prioridad_alta)}).")

print(f"\nDataset extraido en: {carpeta_tarea}")