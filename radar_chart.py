import matplotlib.pyplot as plt
import numpy as np
import os  

def create_radar_chart(team_number, team_data, save_path, color):
    """
    Gera um gráfico radar para o time fornecido.

    Parâmetros:
    - team_number: Número do time (1, 2 ou 3)
    - team_data: Dicionário com os valores médios dos atributos do time
    - save_path: Caminho para salvar a imagem gerada
    - color: Cor principal do gráfico (ex: "red", "blue", "black")
    """
    
    categories = ["Físico", "Defesa", "Tática", "Técnica", "Ataque", "Velocidade"]
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    
    # Adiciona o primeiro valor ao final para fechar o gráfico
    values = [team_data[attr] for attr in categories]
    values += values[:1]  # Fechando o ciclo do gráfico
    angles += angles[:1]  # Fechando o ciclo dos ângulos

    fig, ax = plt.subplots(figsize=(4, 4), subplot_kw=dict(polar=True))  # Ajustado tamanho

    # Preenchendo a área do radar
    ax.fill(angles, values, color=color, alpha=0.3)
    ax.plot(angles, values, color=color, linewidth=1.5, linestyle="-")  # Linha mais visível

    ax.set_ylim(0, 5)  
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_yticklabels(["1", "2", "3", "4", "5"], fontsize=8, color="gray")  

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=9, fontweight="bold")

    # Adicionando título
    ax.set_title(f"Time {team_number}", fontsize=12, fontweight="bold", color=color, pad=15)

    # Criar diretório se não existir
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    # Salvar gráfico
    plt.savefig(save_path, bbox_inches="tight", dpi=300)
    plt.close()
