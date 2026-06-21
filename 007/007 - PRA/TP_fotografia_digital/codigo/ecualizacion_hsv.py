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


def mostrar_canales_rgb(imagen_rgb):
    """Muestra la imagen color y sus tres canales por separado."""
    # Extraemos los tres canales principales.
    canal_rojo = imagen_rgb[:, :, 0]
    canal_verde = imagen_rgb[:, :, 1]
    canal_azul = imagen_rgb[:, :, 2]

    # Creamos una figura de cuatro paneles.
    figura, ejes = plt.subplots(2, 2, figsize=(10, 8), constrained_layout=True)

    # Mostramos la imagen original.
    ejes[0, 0].imshow(imagen_rgb)
    ejes[0, 0].set_title("Imagen original", fontweight="bold", loc="left")
    ejes[0, 0].axis("off")

    # Mostramos el canal rojo.
    ejes[0, 1].imshow(canal_rojo, cmap="gray")
    ejes[0, 1].set_title("Canal rojo", fontweight="bold", loc="left")
    ejes[0, 1].axis("off")

    # Mostramos el canal verde.
    ejes[1, 0].imshow(canal_verde, cmap="gray")
    ejes[1, 0].set_title("Canal verde", fontweight="bold", loc="left")
    ejes[1, 0].axis("off")

    # Mostramos el canal azul.
    ejes[1, 1].imshow(canal_azul, cmap="gray")
    ejes[1, 1].set_title("Canal azul", fontweight="bold", loc="left")
    ejes[1, 1].axis("off")

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


# Parte 1. Camara oscura y procesamiento digital
# Captura con camara oscura + ecualización HSV
nombre_imagen_camara_oscura = "camara_oscura.jpg"

# Inicializamos la variable de imagen para evitar errores si todavia no cargaste el archivo.
imagen_camara_oscura_rgb = None

# Cargamos la imagen solo si escribiste un nombre valido.
if nombre_imagen_camara_oscura != "":
    ruta_camara_oscura = carpeta_imagenes_tp / nombre_imagen_camara_oscura
    imagen_camara_oscura_rgb = cargar_rgb(ruta_camara_oscura)

    # Mostramos la imagen original y su histograma para empezar el diagnostico.
    mostrar_imagen(imagen_camara_oscura_rgb, "Camara oscura: imagen original")
    mostrar_histograma_gris(imagen_camara_oscura_rgb)


imagen_camara_procesada= None
if imagen_camara_oscura_rgb is not None:
    imagen_camara_procesada = imagen_camara_oscura_rgb.copy()

    def recortar_imagen(img, fila_inicial=700, fila_final=1740, columna_inicial=1080, columna_final=3100):
        imagen_recortada = img[fila_inicial:fila_final, columna_inicial:columna_final]

        return imagen_recortada
    
    def voltear_imagen(img, modo=-1):
        """Modo -1 Voltea en ambos ejes,logrando un giro de 180°"""
        imagen_volteada = cv2.flip(img, modo)

        return imagen_volteada
    
    def transformar_perspectiva(img, puntos_origen=None, ancho_salida=1200, alto_salida=600):
            lienzo_destino = np.zeros((alto_salida, ancho_salida,3), dtype=np.uint8)
            if puntos_origen is None:
                puntos_origen = np.array([
                [100, 150],  
                [1800, 130],
                [50, 930],
                [1920, 930] ], dtype=np.float32)
            else:
                puntos_origen= np.float32(puntos_origen)
        
                # Definir puntos de destino
            puntos_destino = np.array([[0,0],[ancho_salida, 0],
                                     [0, alto_salida], [ancho_salida,alto_salida]], dtype=np.float32)
        
            # Matriz de transformacion
            matriz_perspectiva = cv2.getPerspectiveTransform(puntos_origen, puntos_destino)
            imagen_rectificada = cv2.warpPerspective(img, matriz_perspectiva, (ancho_salida, alto_salida))

            return imagen_rectificada
    

    def ecualizar_hsv(img):
        imagen_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(imagen_hsv)
        # Ecualizar solo el brillo (V)
        v_eq = cv2.equalizeHist(v)
        hsv_eq = cv2.merge([h, s, v_eq])
        img_eq_bgr = cv2.cvtColor(hsv_eq, cv2.COLOR_HSV2BGR)
          

        return  img_eq_bgr
    



imagen_camara_procesada = transformar_perspectiva(voltear_imagen(recortar_imagen(imagen_camara_procesada)), ancho_salida=1200, alto_salida=600)
mostrar_imagen(imagen_camara_procesada, "Imagen procesada")
imagen_camara_ecualizada = ecualizar_hsv(imagen_camara_procesada)
mostrar_imagen(imagen_camara_ecualizada, "Imagen ecualizada")

mostrar_histograma_gris(imagen_camara_ecualizada)

# Guardamos imagen ecualizada
imagen_camara_final = imagen_camara_ecualizada


# Guardamos la salida final solo si la imagen existe.
if imagen_camara_final is not None:
    ruta_salida_camara = carpeta_salidas_tp / "camara_ecualizada_final.png"
    guardar_rgb(ruta_salida_camara, imagen_camara_final)

    print(f"Salida guardada en: {ruta_salida_camara.resolve()}")
