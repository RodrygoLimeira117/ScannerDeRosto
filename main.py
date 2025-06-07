# main.py - VERSÃO MODIFICADA
from detector import usar_webcam, usar_imagem
import os

if __name__ == "__main__":
    print("Escolha o modo de processamento:")
    print("1 - Webcam (detecção facial e de emoções em tempo real)")
    print("2 - Imagem (detecção facial e de emoções em uma selfie)")
    escolha = input("Digite 1 ou 2: ").strip()

    if escolha == "1":
        usar_webcam()
    elif escolha == "2":
        # Pede o caminho do arquivo diretamente no terminal
        caminho_imagem = input("Cole o caminho completo do arquivo de imagem e pressione Enter: ").strip()
        
        # Remove aspas extras que podem ser copiadas do Windows
        if caminho_imagem.startswith('"') and caminho_imagem.endswith('"'):
            caminho_imagem = caminho_imagem[1:-1]

        if os.path.exists(caminho_imagem):
            usar_imagem(caminho_imagem) # Passa o caminho para a função
        else:
            print("Erro: Arquivo não encontrado. Verifique se o caminho está correto.")
    else:
        print("Opção inválida. Por favor, digite '1' ou '2'.")