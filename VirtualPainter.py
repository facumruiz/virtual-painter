import cv2
import numpy as np
import mediapipe as mp
import time
import pygame  # Librería para reproducir sonido

class handDetector:
    def __init__(self, mode=False, maxHands=2, detectionCon=0.8, trackCon=0.8):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,
                                        min_detection_confidence=self.detectionCon,
                                        min_tracking_confidence=self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True):
        self.lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
            return self.lmList[8][1], self.lmList[8][2]  # Retorna posición del dedo índice
        return None, None

    def fingersUp(self):
        fingers = []
        if len(self.lmList) > 0:
            if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 1][1]:
                fingers.append(1)  # Pulgar arriba
            else:
                fingers.append(0)
            for id in range(1, 5):
                if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
                    fingers.append(1)  # Dedo levantado
                else:
                    fingers.append(0)  # Dedo abajo
        return fingers

def create_color_palette():
    # Crear un panel de colores
    palette = np.zeros((50, 640, 3), dtype=np.uint8)  # Cambiar la altura a 50
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0),
              (255, 165, 0), (128, 0, 128), (255, 20, 147), (0, 255, 255)]
    for i, color in enumerate(colors):
        cv2.rectangle(palette, (i * 80, 0), ((i + 1) * 80, 50), color, -1)  # Ajustar la altura a 50
    return palette

def main():
    # Inicializar pygame para reproducir sonido
    pygame.mixer.init()
    click_sound = pygame.mixer.Sound("click_sound.wav")
    print("Sonido cargado correctamente.")  # Verificación de que el sonido se cargó

    cap = cv2.VideoCapture(0)
    # Aumentar la resolución de la cámara y establecer fps
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # Ancho de la ventana
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)  # Alto de la ventana
    cap.set(cv2.CAP_PROP_FPS, 60)  # Establecer FPS a 60
    detector = handDetector()
    pTime = 0
    prevX, prevY = None, None
    canvas = None
    positions = []
    # Color inicial del trazo
    current_color = (255, 0, 0)  # Rojo
    palette = create_color_palette()  # Crear paleta de colores
    while True:
        success, img = cap.read()
        if not success:
            break
        img = cv2.flip(img, 1)
        if canvas is None:
            canvas = np.zeros_like(img)
        img = detector.findHands(img)
        x1, y1 = detector.findPosition(img)
        # Dibujar la paleta de colores
        img[0:50, 0:640] = palette  # Ajustar la altura a 50
        if x1 is not None and y1 is not None:
            fingers = detector.fingersUp()
            if fingers[1] == 1 and fingers[2] == 0:  # Solo el dedo índice levantado
                # Comenzamos un nuevo trazo solo si no hay posiciones previas (nuevo inicio)
                if prevX is None and prevY is None:
                    prevX, prevY = x1, y1
                    positions.clear()  # Limpiamos trazos previos para un inicio limpio
                positions.append((x1, y1))
                # Suavizamos posiciones
                if len(positions) > 5:
                    positions.pop(0)
                avg_x = int(sum([p[0] for p in positions]) / len(positions))
                avg_y = int(sum([p[1] for p in positions]) / len(positions))
                if prevX is not None and prevY is not None:
                    # Solo dibuja si hay una posición previa válida
                    current_color = tuple(map(int, current_color))  # Convertir a enteros
                    cv2.line(canvas, (prevX, prevY), (avg_x, avg_y), current_color, 5)
                prevX, prevY = avg_x, avg_y  # Actualiza solo cuando el dedo está levantado
            else:
                # Reinicia las posiciones cuando el dedo no está levantado
                prevX, prevY = None, None
                positions.clear()
        img = cv2.addWeighted(img, 0.5, canvas, 1.0, 0)
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        #cv2.putText(img, f"FPS: {int(fps)}", (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        # Muestra instrucciones
        #cv2.putText(img, "Selecciona un color en la parte superior", (10, 450), cv2.FONT_HERSHEY_PLAIN, 1,
        #            (255, 255, 255), 2)
        cv2.imshow("Image", img)
        # Maneja la selección de color
        if x1 is not None and y1 is not None:
            if y1 < 50:  # Si el dedo está en la parte superior (paleta de colores)
                color_index = x1 // 80  # Determina el índice del color, ajustado para cuadros de 80 píxeles
                if 0 <= color_index < 8:  # Si está dentro de los límites
                    new_color = tuple(palette[0, color_index * 80, :])  # Convertir a enteros
                    if new_color != current_color:  # Cambiar color solo si es diferente
                        current_color = new_color
                        click_sound.play()  # Reproducir sonido
                        print("Color actual:", current_color)  # Para depuración
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
