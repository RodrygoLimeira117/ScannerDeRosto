# main.py - VERSÃO COM TELA DE DETALHES MELHORADA

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import cv2
import os
from PIL import Image, ImageTk
from detector import process_frame_for_gui
import threading

import database

# Variáveis globais
current_image_path = None
analysis_data = None
# Armazena os widgets de progresso para que possam ser destruídos depois
emotion_progress_bars = [] 

# ---- FUNÇÕES DA INTERFACE (com modificações em update_info_tab) ----

def save_result_to_db():
    # ... (Esta função continua a mesma)
    nome_id = name_entry.get().strip()
    if not nome_id:
        messagebox.showerror("Erro", "Por favor, insira um nome para identificar a análise.")
        return
    try:
        database.save_analysis(nome_id, analysis_data)
        messagebox.showinfo("Sucesso", f"Análise para '{nome_id}' salva com sucesso!")
        reset_ui()
        view_history() 
    except Exception as e:
        messagebox.showerror("Erro de Banco de Dados", f"Não foi possível salvar a análise: {e}")

def view_history():
    # ... (Esta função continua a mesma)
    for i in history_tree.get_children():
        history_tree.delete(i)
    try:
        rows = database.get_all_analyses()
        if not rows:
            return
        for row in rows:
            history_tree.insert("", "end", values=row)
    except Exception as e:
        messagebox.showerror("Erro de Banco de Dados", f"Não foi possível carregar o histórico: {e}")

def show_history_details(event):
    # ... (Esta função continua a mesma)
    selected_item = history_tree.focus()
    if not selected_item:
        return
    item_values = history_tree.item(selected_item, "values")
    analysis_id = item_values[0] 
    try:
        past_analysis = database.get_analysis_by_id(analysis_id)
        if past_analysis:
            display_image(past_analysis['caminho_original'])
            update_info_tab(past_analysis)
            notebook.select(info_tab) 
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível carregar detalhes da análise: {e}")

def run_analysis():
    # ... (Esta função continua a mesma)
    global analysis_data
    try:
        n = np.fromfile(current_image_path, np.uint8)
        frame = cv2.imdecode(n, cv2.IMREAD_COLOR)
        if frame is None: raise IOError("Arquivo inválido")
    except Exception as e:
        messagebox.showerror("Erro de Leitura", f"Não foi possível ler o arquivo: {e}")
        reset_ui(); return
    processed_frame_cv2, analysis_data = process_frame_for_gui(frame)
    if analysis_data is None or analysis_data.get('emocao_detectada', 'Nenhuma') == 'Nenhuma':
        messagebox.showwarning("Análise Falhou", "Nenhum rosto ou emoção detectado.")
        reset_ui(); return
    analysis_data["caminho_original"] = current_image_path
    processed_frame_rgb = cv2.cvtColor(processed_frame_cv2, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(processed_frame_rgb)
    display_image(img)
    status_label.config(text=f"Resultado: {analysis_data['emocao_detectada']} ({analysis_data['confianca']})")
    update_info_tab(analysis_data)
    show_save_controls(True)

def update_info_tab(data):
    """
    ---- FUNÇÃO ATUALIZADA ----
    Exibe dados detalhados com um gráfico de barras na aba de informações.
    """
    global emotion_progress_bars

    # Limpa os widgets da análise anterior (labels e barras de progresso)
    for widget in emotion_details_frame.winfo_children():
        widget.destroy()
    emotion_progress_bars = []

    # --- DADOS GERAIS ---
    ttk.Label(emotion_details_frame, text="DETALHES DA ANÁLISE", font=("Helvetica", 12, "bold")).pack(anchor="w")
    ttk.Separator(emotion_details_frame, orient='horizontal').pack(fill='x', pady=5)
    
    file_info = f"Arquivo: {os.path.basename(data.get('caminho_original', 'N/A'))}"
    emotion_info = f"Emoção Dominante: {data.get('emocao_detectada', 'N/A')}"
    
    ttk.Label(emotion_details_frame, text=file_info).pack(anchor="w")
    ttk.Label(emotion_details_frame, text=emotion_info).pack(anchor="w")

    # --- GRÁFICO DE DISTRIBUIÇÃO DE EMOÇÕES ---
    ttk.Label(emotion_details_frame, text="Distribuição de Emoções:", font=("Helvetica", 10, "bold")).pack(anchor="w", pady=(15, 5))
    
    emotions = data.get('emotion', {})
    # Ordena as emoções pelo valor, da maior para a menor
    sorted_emotions = sorted(emotions.items(), key=lambda item: item[1], reverse=True)

    for emotion, value in sorted_emotions:
        # Cria um frame para cada linha (label da emoção + barra)
        row_frame = ttk.Frame(emotion_details_frame)
        row_frame.pack(fill='x', pady=2)

        # Label com o nome da emoção e o valor percentual
        label_text = f"{emotion.capitalize()}: {value:.2f}%"
        label = ttk.Label(row_frame, text=label_text, width=25)
        label.pack(side="left")

        # Barra de progresso para representar o valor visualmente
        progress = ttk.Progressbar(row_frame, orient="horizontal", length=100, mode="determinate", value=value)
        progress.pack(side="left", expand=True, fill='x')
        
        emotion_progress_bars.append((label, progress))

def select_image():
    # ... (Esta função continua a mesma)
    global current_image_path, analysis_data
    filepath = filedialog.askopenfilename(title="Selecione uma imagem", filetypes=[("Imagens", "*.jpg *.jpeg *.png *.bmp")])
    if not filepath: return
    current_image_path = filepath
    analysis_data = None
    reset_ui(clear_image=False)
    display_image(current_image_path)
    status_label.config(text="Analisando... Por favor, aguarde.")
    threading.Thread(target=run_analysis, daemon=True).start()

def reset_ui(clear_image=True):
    global emotion_progress_bars
    if clear_image:
        image_label.config(image=''); image_label.image = None
        image_label_info.config(image=''); image_label_info.image = None
        # Limpa os detalhes da aba de informações
        for widget in emotion_details_frame.winfo_children():
            widget.destroy()
        emotion_progress_bars = []
        
    show_save_controls(False)
    name_entry.delete(0, tk.END)
    status_label.config(text="Selecione uma imagem para começar.")
    select_button.config(state="normal")

def show_save_controls(visible):
    # ... (Esta função continua a mesma)
    if visible: save_frame.pack(pady=10); select_button.config(state="disabled")
    else: save_frame.pack_forget()

def display_image(image_source):
    # ... (Esta função continua a mesma)
    try:
        img = Image.open(image_source) if isinstance(image_source, str) else image_source
        img.thumbnail((220, 220)) # Ajustei o tamanho para o novo layout
        img_tk = ImageTk.PhotoImage(image=img)
        image_label.config(image=img_tk); image_label.image = img_tk
        image_label_info.config(image=img_tk); image_label_info.image = img_tk
    except Exception as e:
        messagebox.showerror("Erro ao Exibir Imagem", f"Não foi possível mostrar a imagem: {e}")
        reset_ui()

# ---- CONFIGURAÇÃO DA JANELA PRINCIPAL ----
root = tk.Tk()
root.title("Analisador de Expressões v2.1 (Detalhes Melhorados)")
root.geometry("600x600") # Aumentei um pouco a janela para o novo layout

style = ttk.Style(root)
style.theme_use("clam")

notebook = ttk.Notebook(root)
notebook.pack(pady=15, padx=15, fill="both", expand=True)

# Abas
analysis_tab = ttk.Frame(notebook)
info_tab = ttk.Frame(notebook)
history_tab = ttk.Frame(notebook)

notebook.add(analysis_tab, text='Análise Principal')
notebook.add(info_tab, text='Detalhes da Análise')
notebook.add(history_tab, text='Histórico')

# ---- WIDGETS DA ABA DE ANÁLISE ----
# ... (Esta seção continua a mesma)
select_button = ttk.Button(analysis_tab, text="1. Selecionar Imagem", command=select_image)
select_button.pack(fill='x', padx=10, pady=10)
status_label = ttk.Label(analysis_tab, text="Selecione uma imagem para começar.", anchor="center", font=("Helvetica", 10))
status_label.pack(pady=5)
image_label = ttk.Label(analysis_tab, anchor="center")
image_label.pack(pady=10)
save_frame = ttk.Frame(analysis_tab)
ttk.Label(save_frame, text="2. Digite um nome e salve a análise:").pack(fill='x')
name_entry = ttk.Entry(save_frame, width=40)
name_entry.pack(pady=5)
buttons_subframe = ttk.Frame(save_frame)
buttons_subframe.pack(pady=5)
ttk.Button(buttons_subframe, text="Salvar Resultado", command=save_result_to_db).pack(side='left', padx=10)
ttk.Button(buttons_subframe, text="Nova Análise", command=reset_ui).pack(side='right', padx=10)
show_save_controls(False)


# ---- WIDGETS DA ABA DE DETALHES (Nova Estrutura) ----
details_main_frame = ttk.Frame(info_tab)
details_main_frame.pack(expand=True, fill="both", padx=10, pady=10)

# Frame da Esquerda para a Imagem
image_frame_info = ttk.Frame(details_main_frame)
image_frame_info.pack(side="left", fill="y", padx=(0, 10))
image_label_info = ttk.Label(image_frame_info, anchor="center")
image_label_info.pack(pady=10)

# Frame da Direita para os Detalhes das Emoções
emotion_details_frame = ttk.Frame(details_main_frame)
emotion_details_frame.pack(side="right", expand=True, fill="both")


# ---- WIDGETS DA ABA DE HISTÓRICO ----
# ... (Esta seção continua a mesma)
ttk.Label(history_tab, text="Dê um duplo-clique em um registro para ver os detalhes.").pack(pady=5)
cols = ("ID", "Nome", "Emoção", "Confiança", "Data")
history_tree = ttk.Treeview(history_tab, columns=cols, show="headings", height=10)
for col in cols:
    history_tree.heading(col, text=col)
    history_tree.column(col, width=80, anchor="center")
history_tree.column("Data", width=120, anchor="center")
history_tree.column("ID", width=40, anchor="center")
history_tree.pack(expand=True, fill="both", padx=10, pady=5)
history_tree.bind("<Double-1>", show_history_details) 

# ---- INICIALIZAÇÃO ----
if __name__ == "__main__":
    import numpy as np 
    database.setup_database()
    view_history()
    root.mainloop()