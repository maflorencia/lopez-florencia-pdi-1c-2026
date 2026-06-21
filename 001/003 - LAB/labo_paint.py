import py5

# Variables globales para controlar el estado del pincel
color_pincel = (255, 0, 0)  # Empezamos con Rojo por defecto (formato RGB)
grosor_pincel = 5

def setup():
    py5.size(800, 600)
    py5.background(255)  # Fondo blanco inicial del lienzo

def draw():
    global color_pincel, grosor_pincel
    
    # --- 1. LÓGICA DE DIBUJO ---
    # Dibujamos solo si el mouse está presionado Y está por debajo de la barra de menú (y > 60)
    if py5.is_mouse_pressed and py5.mouse_y > 60:
        py5.stroke(color_pincel[0], color_pincel[1], color_pincel[2])
        py5.stroke_weight(grosor_pincel)
        # Dibuja una línea continua desde la posición anterior del mouse (pmouse) a la actual
        py5.line(py5.pmouse_x, py5.pmouse_y, py5.mouse_x, py5.mouse_y)
        
    # --- 2. INTERFAZ DE USUARIO (Barra superior) ---
    # La redibujamos constantemente para que el dibujo no tape los botones
    py5.no_stroke()
    py5.fill(230)  # Gris claro para la barra de herramientas
    py5.rect(0, 0, py5.width, 60)
    
    # Configuración general de texto para los botones
    py5.text_align(py5.CENTER, py5.CENTER)
    py5.text_size(12)
    
    # Botón Rojo
    py5.fill(255, 0, 0)
    py5.rect(20, 10, 50, 40)
    
    # Botón Verde
    py5.fill(0, 200, 0)
    py5.rect(80, 10, 50, 40)
    
    # Botón Azul
    py5.fill(0, 0, 255)
    py5.rect(140, 10, 50, 40)
    
    # Botón Borrador (Recuadro blanco con borde gris)
    py5.stroke(180)
    py5.stroke_weight(1)
    py5.fill(255)
    py5.rect(200, 10, 70, 40)
    py5.fill(0)
    py5.no_stroke()
    py5.text("Borrar", 235, 30)
    
    # Botón Limpiar Todo
    py5.stroke(180)
    py5.fill(255)
    py5.rect(280, 10, 100, 40)
    py5.fill(0)
    py5.no_stroke()
    py5.text("Limpiar Todo", 330, 30)


def mouse_pressed():
    """ Esta función detecta de forma automática cuándo hacés un clic individual """
    global color_pincel, grosor_pincel
    
    # Verificamos si el clic ocurrió dentro de la altura de los botones (entre y=10 y y=50)
    if 10 <= py5.mouse_y <= 50:
        
        # Clic en botón Rojo (X entre 20 y 70)
        if 20 <= py5.mouse_x <= 70:
            color_pincel = (255, 0, 0)
            grosor_pincel = 5
            
        # Clic en botón Verde (X entre 80 y 130)
        elif 80 <= py5.mouse_x <= 130:
            color_pincel = (0, 200, 0)
            grosor_pincel = 5
            
        # Clic en botón Azul (X entre 140 y 190)
        elif 140 <= py5.mouse_x <= 190:
            color_pincel = (0, 0, 255)
            grosor_pincel = 5
            
        # Clic en Borrar (X entre 200 y 270) -> Cambia a blanco y aumenta el grosor
        elif 200 <= py5.mouse_x <= 270:
            color_pincel = (255, 255, 255)
            grosor_pincel = 30
            
        # Clic en Limpiar Todo (X entre 280 y 380) -> Pinta un rectángulo blanco sobre el lienzo
        elif 280 <= py5.mouse_x <= 380:
            py5.fill(255)
            py5.no_stroke()
            py5.rect(0, 60, py5.width, py5.height - 60)

# Ejecutar el programa
py5.run_sketch()