# Virtual Painter - Pintor Virtual con OpenCV y MediaPipe

Este proyecto crea una aplicación de "Pintor Virtual" que permite a los usuarios dibujar en la pantalla utilizando gestos de la mano. Con la ayuda de OpenCV y MediaPipe, se rastrea el movimiento de la mano en tiempo real para detectar el dedo índice y permitir que el usuario dibuje en la pantalla y cambiar el color del pincel tocando la paleta de colores.

## Características

- **Dibujo Controlado por Gestos**: Utiliza el dedo índice para dibujar en la pantalla.
- **Paleta de Colores**: Incluye una barra de colores en la parte superior para cambiar el color del dibujo.
- **Retroalimentación en Tiempo Real**: Cambia instantáneamente de color al tocar la paleta.

## Tecnologías Utilizadas

- **Python**: Lenguaje principal del proyecto.
- **OpenCV**: Para captura y procesamiento de imágenes en tiempo real.
- **MediaPipe**: Librería de Google utilizada para la detección y seguimiento de manos.
- **NumPy**: Para manipulación de arrays y cálculos matemáticos.

## Requisitos

Instala las dependencias necesarias antes de ejecutar el programa:

```bash
pip install opencv-python-headless mediapipe numpy

```

## Estructura del Proyecto

```bash
project-directory/
├── virtual_painter.py     # Código principal de la aplicación
└── README.md              # Documentación del proyecto
```

## Ejecucion
1. Clona este repositorio o descarga el archivo principal.
2. Navega hasta el directorio del proyecto.
3. Ejecuta el archivo principal virtual_painter.py:

```bash
python virtual_painter.pys
```

## Uso
* Dibujar: Levanta solo el dedo índice y muévelo sobre la pantalla para comenzar a dibujar.
* Cambio de Color: Toca la barra de colores en la parte superior para cambiar el color del pincel.
* Salir: Presiona la tecla q para cerrar la aplicación.


## Descripción del Código
### Clase handDetector

La clase handDetector es responsable de la detección y seguimiento de manos. Esta clase utiliza MediaPipe para identificar puntos clave en la mano y determinar la posición de los dedos.

### Metodos
* findHands(img, draw=True): Procesa la imagen para detectar manos y dibuja los puntos de referencia.

* findPosition(img, handNo=0, draw=True): Obtiene las coordenadas (x, y) del dedo índice.

* fingersUp(): Devuelve una lista indicando qué dedos están levantados o doblados, útil para interpretar gestos.

### Función create_color_palette
Genera una paleta de colores en la parte superior de la pantalla, lo que permite al usuario seleccionar colores para el dibujo.

### Función main

La función principal del programa realiza las siguientes tareas:

* Configura la cámara y el seguimiento de FPS.

* Procesa el video en tiempo real.

* Detecta la mano y controla la lógica de dibujo en la pantalla.

* Cambia el color al seleccionar uno en la paleta.

