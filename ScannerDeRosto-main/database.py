import sqlite3
from datetime import datetime

DB_NAME = 'analises.db'

def setup_database():
    """Cria o banco de dados e a tabela se não existirem."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS analises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_identificador TEXT NOT NULL,
            emocao_dominante TEXT,
            confianca TEXT,
            caminho_imagem TEXT,
            detalhes_emocoes TEXT,
            data_hora TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_analysis(nome_id, analysis_data):
    """Salva uma nova análise no banco de dados."""
    emocao_dominante = analysis_data.get('emocao_detectada', 'N/A')
    confianca = analysis_data.get('confianca', 'N/A')
    caminho_imagem = analysis_data.get('caminho_original', 'N/A')
    detalhes_emocoes = analysis_data.get('emotion', {})
    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO analises (nome_identificador, emocao_dominante, confianca, caminho_imagem, detalhes_emocoes, data_hora)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (nome_id, emocao_dominante, confianca, caminho_imagem, str(detalhes_emocoes), data_hora))
    conn.commit()
    conn.close()

def get_all_analyses():
    """Busca todos os resumos de análises do banco de dados para o histórico."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome_identificador, emocao_dominante, confianca, data_hora FROM analises ORDER BY data_hora DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_analysis_by_id(analysis_id):
    """Busca uma análise completa pelo seu ID."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT caminho_imagem, emocao_dominante, detalhes_emocoes FROM analises WHERE id = ?", (analysis_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"caminho_original": row[0], "emocao_detectada": row[1], "emotion": eval(row[2])}
    return None