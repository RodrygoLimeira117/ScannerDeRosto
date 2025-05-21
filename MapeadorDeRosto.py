import cv2
import numpy as np
import os

# Carrega o classificador Haar de rosto
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def process_frame(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=7)

    for (x, y, w, h) in faces:
        margin_x = int(w * 0.15)
        margin_y = int(h * 0.10)

        center = (x + w // 2, y + h // 2)
        axis_x = int((w - 2 * margin_x) // 2)
        axis_y = int((h + 2 * margin_y) // 2)

        # Desenha oval verde
        cv2.ellipse(frame, center, (axis_x, axis_y), 0, 0, 360, (0, 255, 0), 2)

        # Máscara para escurecer fora do oval (opcional)
        mask = np.zeros_like(frame)
        cv2.ellipse(mask, center, (axis_x, axis_y), 0, 0, 360, (255, 255, 255), -1)
        frame = cv2.bitwise_and(frame, mask)

    return frame

def usar_webcam():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        processed = process_frame(frame)
        cv2.imshow("Webcam - Pressione Q para sair", processed)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def usar_imagem():
    caminho = input("Digite o caminho da imagem (ex: selfie.jpg): ").strip()

    if not os.path.exists(caminho):
        print("Arquivo não encontrado.")
        return

    imagem = cv2.imread(caminho)
    processed = process_frame(imagem)

    cv2.imshow("Selfie Processada - Pressione qualquer tecla para fechar", processed)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Menu de escolha
print("Escolha o modo:")
print("1 - Webcam")
print("2 - Imagem (selfie)")
escolha = input("Digite 1 ou 2: ").strip()

if escolha == "1":
    usar_webcam()
elif escolha == "2":
    usar_imagem()
else:
    print("Opção inválida.")
