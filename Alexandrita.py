import os
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
import fitz  # PyMuPDF

def carregar_imagens_da_pasta(pasta):
    imagens = []
    for nome_arquivo in os.listdir(pasta):
        if nome_arquivo.endswith(".png") or nome_arquivo.endswith(".jpg") or nome_arquivo.endswith(".jpeg"):
            img = Image.open(os.path.join(pasta, nome_arquivo))
            if img is not None:
                imagens.append((nome_arquivo, img))
    return imagens

def carregar_imagens_de_pdf(caminho_pdf, resolucao=300):
    imagens = []
    documento = fitz.open(caminho_pdf)
    for num_pagina in range(len(documento)):
        pagina = documento.load_page(num_pagina)
        matriz = fitz.Matrix(resolucao / 72, resolucao / 72)  # Define a resolução
        pix = pagina.get_pixmap(matrix=matriz)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        imagens.append((f"pagina_{num_pagina+1}.png", img))
    return imagens, len(documento)

def substituir_cores(img, cor_fundo, cor_caneta, tolerancia_fundo=60, tolerancia_caneta=60):
    img_np = np.array(img)
    
    # Converter cores alvo para arrays numpy
    cor_fundo_np = np.array(cor_fundo)
    cor_caneta_np = np.array(cor_caneta)
    
    # Calcular máscara para a cor de fundo
    mascara_fundo = np.all(np.abs(img_np - cor_fundo_np) <= tolerancia_fundo, axis=-1)
    
    # Calcular máscara para a cor da caneta
    mascara_caneta = np.all(np.abs(img_np - cor_caneta_np) <= tolerancia_caneta, axis=-1)
    
    # Criar uma nova imagem para a saída
    output_img_np = np.copy(img_np)
    
    # Definir a cor de fundo
    Base= [30, 30, 46]
    Mantle=[24, 24, 37]
    Crust=[17, 17, 27]
    #escolha a cor de fundo
    output_img_np[mascara_fundo] = Base
    
    # Definir a cor da caneta com paletas do catppuccin Mocha
    Rosewater=[245, 224, 220]
    Flamingo=[242, 205, 205]
    Pink=[245, 194, 231]
    Mauve=[203, 166, 247]
    Red=[243, 139, 168]
    Maroon=[235, 160, 172]
    Peach=[250, 179, 135]
    Yellow=[249, 226, 175]
    Green =[166, 227, 161]
    Teal= [148, 226, 213]
    Sky= [137, 220, 235]
    Saphire = [116, 199, 236]
    Blue = [137, 180, 250]

    #Escreva abaixo a cor que você escolheu ou coloque a cor em notação rgb que você quiser
    output_img_np[mascara_caneta] = Saphire
    
    # Converter de volta para uma imagem
    output_img = Image.fromarray(output_img_np)
    return output_img

def melhorar_caligrafia(img):
    # Converter para escala de cinza
    cinza = img.convert("L")
    # Aumentar o contraste
    aprimorador = ImageEnhance.Contrast(cinza)
    img_aprimorada = aprimorador.enhance(2)
    # Aplicar filtro de nitidez
    img_nitida = img_aprimorada.filter(ImageFilter.SHARPEN)
    # Converter de volta para RGB
    return img_nitida.convert("RGB")

def binarizar_imagem(img, limiar=128):
    cinza = img.convert("L")
    binarizada = cinza.point(lambda x: 255 if x > limiar else 0, mode='1')
    return binarizada.convert("RGB")

def processar_imagens(pasta_entrada, pasta_saida, resolucao_pdf=300):
    print(f"Carregando imagens da pasta: {pasta_entrada}")
    imagens = []
    arquivos_pdf = []
    
    for nome_arquivo in os.listdir(pasta_entrada):
        if nome_arquivo.endswith(".pdf"):
            imagens_pdf, num_paginas = carregar_imagens_de_pdf(os.path.join(pasta_entrada, nome_arquivo), resolucao=resolucao_pdf)
            imagens.extend(imagens_pdf)
            arquivos_pdf.append((nome_arquivo, num_paginas))
        else:
            img = Image.open(os.path.join(pasta_entrada, nome_arquivo))
            if img is not None:
                imagens.append((nome_arquivo, img))
    
    # Garantir que a pasta de saída exista
    if not os.path.exists(pasta_saida):
        os.makedirs(pasta_saida)
    
    if not imagens:
        print("Nenhuma imagem encontrada na pasta de entrada.")
        return

    imagens_processadas = []

    for nome_arquivo, img in imagens:
        print(f"Processando imagem: {nome_arquivo}")
        
        # Melhorar a caligrafia
        img_aprimorada = melhorar_caligrafia(img)
        
        # Binarizar imagem
        img_binarizada = binarizar_imagem(img_aprimorada)
        
        # Estimar a cor de fundo
        cor_fundo = estimar_cor_fundo(img_binarizada)
        print(f"Cor de fundo estimada para {nome_arquivo}: {cor_fundo}")
        
        # Estimar a cor da caneta (isso pode ser complicado e pode precisar de lógica adicional)
        cor_caneta = [0, 0, 0]  # Assumindo que a cor da caneta é próxima do preto
        
        # Substituir cores
        img_processada = substituir_cores(img_binarizada, cor_fundo, cor_caneta)
        
        # Salvar a imagem processada
        caminho_saida = os.path.join(pasta_saida, nome_arquivo)
        img_processada.save(caminho_saida)
        imagens_processadas.append((nome_arquivo, img_processada))
        print(f"Imagem salva em: {caminho_saida}")

    # Combinar imagens de volta em PDFs se a entrada era um PDF
    for nome_pdf, num_paginas in arquivos_pdf:
        imagens_pdf = [img for nome, img in imagens_processadas if nome.startswith("pagina_")]
        caminho_pdf_saida = os.path.join(pasta_saida, nome_pdf.replace(".pdf", "_processado.pdf"))
        imagens_pdf[0].save(caminho_pdf_saida, save_all=True, append_images=imagens_pdf[1:])
        print(f"PDF salvo em: {caminho_pdf_saida}")

def estimar_cor_fundo(img):
    img_np = np.array(img)
    pixels = img_np.reshape(-1, 3)
    unico, contagens = np.unique(pixels, axis=0, return_counts=True)
    cor_fundo = unico[np.argmax(contagens)]
    return cor_fundo

# Definir as pastas de entrada e saída
pasta_entrada = '/home/daniel/Documentos/python/Processamento de imagem/entrada'
pasta_saida = '/home/daniel/Documentos/python/Processamento de imagem/saida'

# Processar as imagens
processar_imagens(pasta_entrada, pasta_saida)
