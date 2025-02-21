import matplotlib.pyplot as plt
import numpy as np
import os
from PIL import Image, ImageDraw, ImageFont

def create_text_image(players, team_number, fig_size, color):
    """
    Cria uma imagem separada com a lista de jogadores do time.

    Parâmetros:
    - players: Lista de jogadores.
    - team_number: Número do time (para título).
    - fig_size: Tamanho da figura (definida pelo usuário).
    - color: Cor do time (ex: "red", "blue", "black").

    Retorna:
    - Caminho da imagem gerada.
    """
    # Definindo as cores mais escuras
    dark_colors = {
        "red": (180, 0, 0),  # Vermelho mais escuro
        "blue": (0, 0, 180),  # Azul mais escuro
        "black": (0, 0, 0)  # Preto (já escuro)
    }

    # Atribuir a cor correspondente mais escura
    dark_red = dark_colors["red"]
    dark_blue = dark_colors["blue"]
    dark_black = dark_colors["black"]

    width = fig_size
    height = fig_size
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)

    # Fonte personalizada
    try:
        font = ImageFont.truetype("Times_New_Roman_Bold.ttf", int(fig_size * 0.08))  # Fonte proporcional ao tamanho da imagem
    except:
        font = ImageFont.load_default()

    # Mapeamento das cores em inglês para português
    color_translation = {
        "red": "Vermelho",
        "blue": "Azul",
        "black": "Preto"
    }

    # Escolher a cor escura para o título e os jogadores com base no time
    if color == "red":
        title_color = dark_red
        player_color = dark_red
    elif color == "blue":
        title_color = dark_blue
        player_color = dark_blue
    else:
        title_color = dark_black
        player_color = dark_black

    # Posicionamento do título
    title_y = int(fig_size * 0.05)
    draw.text((width // 4, title_y), f"Time {team_number} ({color_translation.get(color, color)})", fill=title_color, font=font)

    # Posicionamento dos jogadores
    text_y = title_y + int(fig_size * 0.1)
    line_spacing = int(fig_size * 0.08)

    for player in players:
        draw.text((width // 6, text_y), f"- {player}", fill=player_color, font=font)
        text_y += line_spacing

    # Criar diretório se não existir
    os.makedirs("generated", exist_ok=True)
    img_path = f"generated/team_{team_number}_list.png"
    img.save(img_path)
    return img_path


def create_combined_image(team_images, team_players, save_path, fig_size):
    """
    Cria uma imagem combinada organizando os radares e listas em um layout 2xN.

    Parâmetros:
    - team_images: Lista com os caminhos das imagens dos radares.
    - team_players: Lista com listas de jogadores de cada time.
    - save_path: Caminho onde a imagem final será salva.
    - fig_size: Tamanho das figuras (ajustável).
    """
    num_teams = len(team_images)
    
    # Criar imagens das listas de jogadores
    list_images = []
    colors = ["red", "blue", "black"]  # Cores para os times

    for i, (players, color) in enumerate(zip(team_players, colors)):
        list_img = create_text_image(players, i + 1, fig_size, color)  # Passar a cor de cada time
        list_images.append(list_img)

    # Definir tamanho final da imagem combinada
    combined_width = 2 * fig_size
    combined_height = num_teams * fig_size
    combined_img = Image.new("RGB", (combined_width, combined_height), "white")

    # Adicionar listas e radares à imagem final
    for i in range(num_teams):
        list_img = Image.open(list_images[i])
        radar_img = Image.open(team_images[i])

        combined_img.paste(list_img, (0, i * fig_size))  # Coluna 1 (listas)
        combined_img.paste(radar_img, (fig_size, i * fig_size))  # Coluna 2 (radares)

    # Criar diretório se não existir
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    # Salvar imagem final
    combined_img.save(save_path)
