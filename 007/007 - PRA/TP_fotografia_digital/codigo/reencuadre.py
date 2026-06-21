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

    # ___________________________________________________________
# ___________________________________________________________
# Parte 2. Composición y lenguaje visual.
# 2.2 Reencuadre y reinterpretación


nombre_imagen_reencuadre = "imagen_reencuadre.jpg"

# Inicializamos la variable de imagen para evitar errores si todavia no cargaste el archivo.
imagen_reencuadre_rgb = None

# Cargamos la imagen solo si escribiste un nombre valido.
if nombre_imagen_reencuadre != "":
    ruta_camara_oscura = carpeta_imagenes_tp / nombre_imagen_reencuadre
    imagen_reencuadre_rgb = cargar_rgb(ruta_camara_oscura)

    # Mostramos la imagen original y su histograma para empezar el diagnostico.
    mostrar_imagen(imagen_reencuadre_rgb, "Imagen Original")
    mostrar_histograma_gris(imagen_reencuadre_rgb)

def recortar_imagen(img, fila_inicial, fila_final, columna_inicial, columna_final):
        imagen_recortada = img[fila_inicial:fila_final, columna_inicial:columna_final]

        return imagen_recortada

recorte_a = imagen_reencuadre_rgb
recorte_a = recortar_imagen(recorte_a, fila_inicial=500, fila_final=3010, columna_inicial=295, columna_final=3024)
mostrar_imagen(recorte_a, "Recorte A")


recorte_b = imagen_reencuadre_rgb
recorte_b = recortar_imagen(recorte_b, fila_inicial=685, fila_final=2970, columna_inicial=690, columna_final=2275)
mostrar_imagen(recorte_b, "Recorte B")

def previsualizar_multiples_recortes(img, lista_recortes):
   
    copia = img.copy()
    
    for rec in lista_recortes:
        # Extraemos coordenadas
        y_ini, y_fin = rec['y']
        x_ini, x_fin = rec['x']
        color = rec.get('color', (255, 0, 0)) 
        
        # Dibujamos el rectángulo (OpenCV usa X, Y)
        cv2.rectangle(copia, (x_ini, y_ini), (x_fin, y_fin), color, 20)
        
        # Opcional: Agregar texto sobre el recuadro
        cv2.putText(copia, rec.get('label', ''), (x_ini, y_ini - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, color, 5)

    plt.figure(figsize=(12, 8))
    plt.imshow(copia) # Si tu imagen es RGB, se verá bien
    plt.title("Recortes de zonas A y B",  fontweight="bold", loc="left")
    plt.axis('off')
    plt.show()


zonas_recorte = [
    {
        'label': 'Recorte A',
        'y': (500, 3010), 
        'x': (295, 3024), 
        'color': (255, 0, 0) 
    },
    {
        'label': 'Recorte B',
        'y': (685, 2970), 
        'x': (690, 2275), 
        'color': (0, 0, 255) 
    }
]

previsualizar_multiples_recortes(imagen_reencuadre_rgb, zonas_recorte)