import cv2
import os
from emotion import analisar_emocao
from utils import desenhar_elipse, carregar_cascata, get_face_detector, TEXT_COLOR, FONT, LINE_THICKNESS
import logging
# As importações do tkinter não são mais necessárias aqui
# from tkinter import Tk
# from tkinter.filedialog import askopenfilename

FACE_CASCADE = carregar_cascata()

def process_frame(frame, use_deepface=False):
    display_frame = frame.copy()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces_dlib = get_face_detector()(gray)
    detected_faces_coords = [(f.left(), f.top(), f.width(), f.height()) for f in faces_dlib]

    for (x, y, w, h) in detected_faces_coords:
        desenhar_elipse(display_frame, x, y, w, h)
        if use_deepface:
            face_roi = frame[max(0, y):min(frame.shape[0], y+h), max(0, x):min(frame.shape[1], x+w)]
            if face_roi.size > 0:
                emocao = analisar_emocao(face_roi)
                if emocao:
                    text = f"{emocao['dominant_emotion']} ({emocao['confidence']:.2f}%)"
                    cv2.putText(display_frame, text, (x, y - 10), FONT, 0.9, TEXT_COLOR, LINE_THICKNESS, cv2.LINE_AA)
    return display_frame

def usar_webcam():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Erro: Não foi possível abrir a webcam.")
        return

    print("Webcam ativada. Pressione 'q' para sair.")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Falha ao capturar o frame da webcam.")
            break

        processed_frame = process_frame(frame, use_deepface=True)
        cv2.imshow("Webcam - Pressione Q para sair", processed_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# A função agora recebe o caminho da imagem como um argumento
def usar_imagem(caminho_imagem):
    try:
        imagem = cv2.imread(caminho_imagem)
        if imagem is None:
            print(f"Erro ao carregar a imagem: {caminho_imagem}")
            return

        processed = process_frame(imagem, use_deepface=True)
        nome_arquivo = os.path.basename(caminho_imagem)
        cv2.imshow(f"Imagem: {nome_arquivo}", processed)
        
        print("Análise concluída. Pressione qualquer tecla na janela da imagem para fechar.")
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    except Exception as e:
        print(f"Ocorreu um erro ao processar a imagem: {e}")