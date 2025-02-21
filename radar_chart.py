import matplotlib.pyplot as plt
import numpy as np
import os  # Adicionado para manipulação de diretórios

def create_radar_chart(team_number, team_data, save_path, color):
    """
    Gera um gráfico radar para o time fornecido.

    Parâmetros:
    - team_number: Número do time (1, 2 ou 3)
    - team_data: Dicionário com os valores médios dos atributos do time
    - save_path: Caminho para salvar a imagem gerada
    - color: Cor principal do gráfico (ex: "red", "blue", "black")
    """
    categories = ["Técnica", "Ataque", "Velocidade", "Físico", "Defesa", "Tática"]
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    
    # Adiciona o primeiro valor ao final para fechar o gráfico
    values = [team_data[attr] for attr in categories]
    values += values[:1]  # Fechando o ciclo do gráfico
    angles += angles[:1]  # Fechando o ciclo dos ângulos

    fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))
    ax.fill(angles, values, color=color, alpha=0.3)
    ax.plot(angles, values, color=color, linewidth=2)

    ax.set_ylim(0, 5)
    ax.set_yticks([1, 2, 3, 4, 5])

    ax.set_xticks(angles[:-1])  # Definir as posições das categorias no eixo circular
    ax.set_xticklabels(categories, fontsize=10, fontweight="bold")

    team_name = f"Time {team_number}"
    ax.set_title(team_name, color=color, fontsize=14, fontweight="bold", pad=20)

    # 🔹 Criar o diretório "generated" se não existir
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    plt.savefig(save_path, bbox_inches="tight", dpi=300)
    plt.close()
