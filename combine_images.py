import matplotlib.pyplot as plt
import os
from PIL import Image, ImageDraw, ImageFont

def create_combined_image(team1_img, team2_img, team1_players, team2_players, save_path):
    """
    Combina as imagens dos radares e as listas de jogadores em um layout 2x2.

    Parâmetros:
    - team1_img: Caminho da imagem do radar do Time 1
    - team2_img: Caminho da imagem do radar do Time 2
    - team1_players: Lista de jogadores do Time 1
    - team2_players: Lista de jogadores do Time 2
    - save_path: Caminho onde a imagem final será salva.
    """
    # Carregar imagens dos radares
    img1 = Image.open(team1_img)
    img2 = Image.open(team2_img)

    # Definir tamanho da imagem combinada
    width, height = img1.size
    combined_width = 2 * width
    combined_height = 2 * height

    # Criar imagem branca
    combined_img = Image.new("RGB", (combined_width, combined_height), "white")

    # Adicionar radares às posições (1,1) e (2,1)
    combined_img.paste(img1, (0, 0))
    combined_img.paste(img2, (0, height))

    # Criar um objeto para desenhar na imagem
    draw = ImageDraw.Draw(combined_img)

    # Fonte para os textos (ajuste para o caminho correto caso necessário)
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except:
        font = ImageFont.load_default()

    # Posição inicial para os textos
    text_x = width + 20
    text_y_1 = 20
    text_y_2 = height + 20

    # Desenhar títulos
    draw.text((text_x, text_y_1 - 30), "Time 1", fill="black", font=font)
    draw.text((text_x, text_y_2 - 30), "Time 2", fill="black", font=font)

    # Adicionar nomes dos jogadores
    for i, player in enumerate(team1_players):
        draw.text((text_x, text_y_1 + i * 25), player, fill="black", font=font)

    for i, player in enumerate(team2_players):
        draw.text((text_x, text_y_2 + i * 25), player, fill="black", font=font)

    # Criar diretório se não existir
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    # Salvar imagem final
    combined_img.save(save_path)
