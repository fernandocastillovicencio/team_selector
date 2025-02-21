import streamlit as st
import pandas as pd
import numpy as np
from process import parse_players, normalize_name, process_players_in_database
from balance import balance_teams
from radar_chart import create_radar_chart
from combine_images import create_combined_image
from team_selection import calcular_diferenca_mg  

# 🔹 Configuração da Página
st.set_page_config(page_title="Times da Pelega", layout="centered")
st.image("assets/logo.png", width=200)
st.title("Times da Pelega")

# 🔹 Entrada da lista de jogadores
st.subheader("Lista de Jogadores")
player_input = st.text_area("Cole a lista de jogadores aqui", height=500)

# 🔹 Seleção do número de times
num_teams = st.radio("Número de Times:", [2, 3])

# 🔹 Definição do número de combinações avaliadas (até 1000)
num_combinacoes = st.number_input("Número de Times Avaliados (N)", min_value=1, max_value=3000, value=100, step=100)

# 🔹 Botão para formar os times
if st.button("FAZER TIMES"):
    if not player_input.strip():
        st.warning("Insira a lista de jogadores antes de continuar.")
    else:
        # 🔹 Processa o texto para obter a lista única de jogadores
        jogadores = parse_players(player_input)

        # 🔹 Carregar a base de dados dos jogadores
        df_base = pd.read_csv("data/players.csv")
        df_base.rename(columns={"Jogador": "Nome"}, inplace=True)
        df_base["Nome"] = df_base["Nome"].apply(normalize_name)

        # 🔹 Processa a busca na base de dados
        matched_players, unrecognized_players = process_players_in_database(jogadores, df_base)

        # 🔹 Criar DataFrame para armazenar os resultados de todas as combinações
        resultados = []

        # 🔹 Criar barra de progresso
        progress_bar = st.progress(0)

        # 🔹 Gerar N combinações e avaliar a melhor
        melhor_diff = float("inf")
        melhor_times = None
        melhor_medias = None

        for i in range(num_combinacoes):
            teams = balance_teams(pd.DataFrame(matched_players), num_teams=num_teams)
            medias, diff = calcular_diferenca_mg(teams, pd.DataFrame(matched_players))

            # Salvar os resultados
            resultados.append({
                "Iteração": i + 1,
                "Times": teams,
                "Médias": medias,
                "Diferença MG": diff
            })

            # Atualizar se for a melhor combinação
            if diff < melhor_diff:
                melhor_diff = diff
                melhor_times = teams
                melhor_medias = medias

            # Atualizar barra de progresso
            progress_bar.progress((i + 1) / num_combinacoes)

        # Criar DataFrame com os resultados
        df_resultados = pd.DataFrame(resultados)

        print("\nResultados das combinações geradas:")
        print(df_resultados[["Iteração", "Diferença MG"]].head(20))  # Mostrar apenas as 20 primeiras linhas no terminal

        # 🔹 Mapeamento de cores
        cores_times = {1: "Vermelho", 2: "Azul", 3: "Preto"}

        # 🔹 Exibir título final antes dos gráficos
        st.subheader("Melhor Configuração")

        # 🔹 Exibir as médias da melhor configuração com cores
        for i, media in enumerate(melhor_medias):
            st.write(f"**Time {i+1} ({cores_times[i+1]}):** {media:.3f}")

        # 🔹 Exibir diferença de MG final
        st.write(f"**Diferença Total:** {melhor_diff:.3f}")

        # 🔹 Gerar gráficos radar para os melhores times
        colors = ["red", "blue", "black"]
        image_paths = []
        team_lists = []

        for i, team in melhor_times.items():
            team_number = i + 1

            # 🔹 Calcular média dos atributos para o time
            team_data = {attr: pd.DataFrame(matched_players)[pd.DataFrame(matched_players)['Nome'].isin(team)][attr].mean() 
                         for attr in ["Físico", "Defesa", "Tática", "Técnica", "Ataque", "Velocidade"]}

            # 🔹 Gerar e salvar gráfico de radar do time
            image_path = f"generated/team_{team_number}.png"
            create_radar_chart(team_number, team_data, image_path, color=colors[i])
            
            image_paths.append(image_path)
            team_lists.append(team)

        # 🔹 Criar imagem combinada com listas + radares
        fig_size = 520  
        combined_image_path = "generated/combined_teams.png"
        create_combined_image(image_paths, team_lists, combined_image_path, fig_size)

        # 🔹 Exibir a imagem combinada no Streamlit
        st.image(combined_image_path, caption="Melhor Configuração de Times", width=700)

        # 🔹 Botão para baixar a imagem final
        with open(combined_image_path, "rb") as file:
            st.download_button(label="Baixar Imagem dos Times", data=file, file_name="times_combinados.png", mime="image/png")
