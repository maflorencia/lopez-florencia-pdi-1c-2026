# Importamos herramientas de rutas para manejar archivos de entrada y salida.
from pathlib import Path

# Importamos OpenCV para cargar y transformar imagenes.
import cv2

# Importamos NumPy para trabajar con matrices y mascaras.
import numpy as np

# Importamos Pandas para construir la tabla final del trabajo.
import pandas as pd

# Importamos Matplotlib para mostrar comparaciones dentro del notebook.
import matplotlib.pyplot as plt

# Definimos la carpeta donde vas a guardar tus imagenes originales.
carpeta_imagenes_tp = Path("006_fotografia_digital/imagenes/originales")

# Definimos la carpeta donde vas a guardar los resultados finales.
carpeta_salidas_tp = Path("006_fotografia_digital/imagenes/procesadas")

print(f"Carpeta esperada para originales: {carpeta_imagenes_tp.resolve()}")
print(f"Carpeta esperada para resultados: {carpeta_salidas_tp.resolve()}")

# Funciones

def cargar_rgb(ruta):
    """Abre una imagen color y la devuelve en formato RGB."""
    # Leemos la imagen con OpenCV en formato BGR.
    imagen_bgr = cv2.imread(str(ruta), cv2.IMREAD_COLOR)

    # Verificamos que la lectura haya sido correcta.
    if imagen_bgr is None:
        raise FileNotFoundError(f"No se pudo leer la imagen: {ruta}")

    # Convertimos de BGR a RGB para visualizar correctamente con Matplotlib.
    imagen_rgb = cv2.cvtColor(imagen_bgr, cv2.COLOR_BGR2RGB)
    return imagen_rgb

def cargar_gris(ruta):
    """Abre una imagen en escala de grises."""
    # Leemos la imagen directamente como grises.
    imagen_gris = cv2.imread(str(ruta), cv2.IMREAD_GRAYSCALE)

    # Verificamos que la lectura haya sido correcta.
    if imagen_gris is None:
        raise FileNotFoundError(f"No se pudo leer la imagen: {ruta}")

    return imagen_gris


def mostrar_imagen(imagen, titulo="Imagen"):
    """Muestra una sola imagen con un titulo."""
    # Definimos el tamano general de la figura.
    plt.figure(figsize=(7, 6), constrained_layout=True)

    # Elegimos el mapa de color segun la cantidad de dimensiones.
    mapa_de_color = None
    if imagen.ndim == 2:
        mapa_de_color = "gray"

    # Dibujamos la imagen y su titulo.
    plt.imshow(imagen, cmap=mapa_de_color)
    plt.title(titulo,fontweight="bold", loc="left")
    plt.axis("on")
    plt.show()


def mostrar_comparacion(imagen_izquierda, imagen_derecha, titulo_izquierda, titulo_derecha):
    """Muestra una comparacion simple entre dos imagenes."""
    # Creamos una figura con dos ejes lado a lado.
    figura, ejes = plt.subplots(1, 2, figsize=(12, 5), constrained_layout=True)

    # Definimos el mapa de color para la imagen izquierda.
    mapa_izquierda = None
    if imagen_izquierda.ndim == 2:
        mapa_izquierda = "gray"

    # Dibujamos la imagen izquierda.
    ejes[0].imshow(imagen_izquierda, cmap=mapa_izquierda)
    ejes[0].set_title(titulo_izquierda, fontweight="bold", loc="left")
    ejes[0].axis("off")

    # Definimos el mapa de color para la imagen derecha.
    mapa_derecha = None
    if imagen_derecha.ndim == 2:
        mapa_derecha = "gray"

    # Dibujamos la imagen derecha.
    ejes[1].imshow(imagen_derecha, cmap=mapa_derecha)
    ejes[1].set_title(titulo_derecha, fontweight="bold", loc="left")
    ejes[1].axis("off")

    plt.show()


def mostrar_histograma_gris(imagen):
    """Muestra el histograma en grises de una imagen color o gris."""
    # Convertimos a grises si la imagen viene en color.
    imagen_gris = imagen
    if imagen.ndim == 3:
        imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_RGB2GRAY)

    # Calculamos el histograma con NumPy.
    histograma, bordes = np.histogram(imagen_gris.flatten(), bins=256, range=[0, 256])

    # Dibujamos la curva del histograma.
    plt.figure(figsize=(10, 4), constrained_layout=True)
    plt.plot(bordes[:-1], histograma, color="black")
    plt.title("Histograma en escala de grises", fontweight="bold", loc="left")
    plt.xlabel("Intensidad")
    plt.ylabel("Cantidad de pixeles")
    plt.xlim(0, 255)
    plt.grid(alpha=0.3)
    plt.show()

def calcular_histograma_rgb(imagen):
    canales = ('b', 'g', 'r')
    colores = ('blue', 'green', 'red')
    
    plt.figure(figsize=(10, 5), constrained_layout=True)
    plt.title('Histograma RGB', fontweight="bold", loc="left")
    plt.xlabel('Intensidad de píxel (0-255)')
    plt.ylabel('Cantidad de píxeles')

    
    for i, col in enumerate(canales):
        # cv2.calcHist(imágenes, canales, máscara, tamañoHist, rango)
        hist = cv2.calcHist([imagen], [i], None, [256], [0, 256])
        
        # Graficamos cada canal con su color correspondiente
        plt.plot(hist, color=colores[i], label=f'Canal {col.upper()}')
        plt.xlim([0, 256])
    
    plt.legend()
    plt.show()



def guardar_rgb(ruta_salida, imagen_rgb):
    """Guarda una imagen RGB en disco."""
    # Convertimos la imagen a BGR para que OpenCV la guarde correctamente.
    imagen_bgr = cv2.cvtColor(imagen_rgb, cv2.COLOR_RGB2BGR)

    # Guardamos la imagen en la ruta indicada.
    cv2.imwrite(str(ruta_salida), imagen_bgr)


def guardar_gris(ruta_salida, imagen_gris):
    """Guarda una imagen en escala de grises."""
    # Guardamos la imagen directamente en la ruta indicada.
    cv2.imwrite(str(ruta_salida), imagen_gris)


# ___________________________________________________________
# ___________________________________________________________
# Parte 2. Composición y lenguaje visual.
# 2.1 Fotografía de simplicidad visual

nombre_imagen_simplicidad = "camara_simplicidad.jpg"

# Inicializamos la variable de imagen para evitar errores si todavia no cargaste el archivo.
imagen_simplicidad_rgb = None

# Cargamos la imagen solo si escribiste un nombre valido.
if nombre_imagen_simplicidad != "":
    ruta_camara_oscura = carpeta_imagenes_tp / nombre_imagen_simplicidad
    imagen_simplicidad_rgb = cargar_rgb(ruta_camara_oscura)

    # Mostramos la imagen original y su histograma para empezar el diagnostico.
    mostrar_imagen(imagen_simplicidad_rgb, "Imagen Original")
    mostrar_histograma_gris(imagen_simplicidad_rgb)


def recortar_imagen(img, fila_inicial=10, fila_final=3750, columna_inicial=203, columna_final=2900):
        imagen_recortada = img[fila_inicial:fila_final, columna_inicial:columna_final]

        return imagen_recortada

def convertir_grises(img):
    gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return gris

imagen_simplicidad_rgb = recortar_imagen(imagen_simplicidad_rgb)
imagen_simplicidad_grises= convertir_grises(imagen_simplicidad_rgb)
mostrar_imagen(imagen_simplicidad_grises, "Imagen en escala de grises")


# Version final para este caso.
imagen_grises_final = imagen_simplicidad_grises

# Guardamos la salida final solo si la imagen existe.
if imagen_grises_final is not None:
    ruta_salida_grises = carpeta_salidas_tp / "imagen_grises_final.png"
    guardar_gris(ruta_salida_grises, imagen_grises_final)

    print(f"Salida guardada en: {ruta_salida_grises.resolve()}")

mostrar_histograma_gris(imagen_grises_final)