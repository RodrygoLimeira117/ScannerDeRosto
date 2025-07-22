# detector.py - VERSÃO FINAL

import cv2
from emotion import analisar_emocao
from utils import desenhar_elipse, get_face_detector, TEXT_COLOR, FONT, LINE_THICKNESS

def process_frame_for_gui(frame):
    """
    Processa um frame, adiciona padding ao rosto recortado para melhorar a
    detecção de emoção e retorna a imagem processada e os resultados.
    """
    processed_frame = frame.copy()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces_dlib = get_face_detector()(gray)
    
    if not faces_dlib:
        return frame, None

    face = faces_dlib[0]
    x, y, w, h = face.left(), face.top(), face.width(), face.height()

    desenhar_elipse(processed_frame, x, y, w, h)

    analysis_result = {
        "caminho_original": None,
        "nome_identificador": None,
        "emocao_detectada": "Nenhuma",
        "confianca": 0,
        "emotion": {}
    }

    # Adiciona um padding (margem) ao redor do rosto
    padding_y = int(h * 0.30)
    padding_x = int(w * 0.30)
    y1 = max(0, y - padding_y)
    y2 = min(frame.shape[0], y + h + padding_y)
    x1 = max(0, x - padding_x)
    x2 = min(frame.shape[1], x + w + padding_x)
    face_roi = frame[y1:y2, x1:x2]

    if face_roi.size > 0:
        emocao = analisar_emocao(face_roi) 
            
        if emocao:
            dominant_emotion = emocao['dominant_emotion']
            confidence_value = emocao['emotion'][dominant_emotion]

            analysis_result["emocao_detectada"] = dominant_emotion
            analysis_result["confianca"] = f"{confidence_value:.2f}%"
            analysis_result['emotion'] = emocao.get('emotion', {})
            
            text = f"{dominant_emotion} ({confidence_value:.2f}%)"
            cv2.putText(processed_frame, text, (x, y - 10), FONT, 0.9, TEXT_COLOR, LINE_THICKNESS, cv2.LINE_AA)
            
    return processed_frame, analysis_result