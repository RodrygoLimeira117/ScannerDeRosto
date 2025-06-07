from deepface import DeepFace
import logging

def analisar_emocao(face_roi):
    try:
        analysis = DeepFace.analyze(face_roi, actions=['emotion'], enforce_detection=False, prog_bar=False)
        if analysis and isinstance(analysis, list) and len(analysis) > 0:
            dominant_emotion = analysis[0]['dominant_emotion']
            confidence = analysis[0]['emotion'][dominant_emotion]
            return {'dominant_emotion': dominant_emotion, 'confidence': confidence}
    except Exception as e:
        logging.warning(f"Erro na análise de emoção: {e}")
    return None