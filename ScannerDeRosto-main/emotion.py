# emotion.py - VERSÃO FINAL

from deepface import DeepFace
import logging

def analisar_emocao(face_roi):
    """
    Analisa uma região de rosto e retorna o dicionário completo da análise.
    """
    try:
        # A chamada foi simplificada para ser compatível com sua versão da biblioteca.
        # O argumento 'prog_bar' foi removido.
        analysis = DeepFace.analyze(
            img_path=face_roi,
            actions=['emotion'],
            enforce_detection=True
        )
        if analysis and isinstance(analysis, list) and len(analysis) > 0:
            return analysis[0]
            
    except Exception as e:
        # Mantemos um log para o caso de erros futuros, mas sem interromper o programa.
        logging.warning(f"Erro na análise de emoção: {e}")
        
    return None