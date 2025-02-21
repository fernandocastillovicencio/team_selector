import streamlit as st
import pandas as pd
import os
from process import parse_players, normalize_name
from balance import balance_teams
from radar_chart import create_radar_chart

# Carregar base de dados dos jogadores
df_base = pd.read_csv("data/players.csv")

# Renomear a coluna "Jogador" para "Nome" para manter a compatibilidade no código
df_base.rename(columns={"Jogador": "Nome"}, inplace=True)

# Normalizar os nomes no DataFrame para evitar problemas de comparação
df_base["Nome"] = df_base["Nome"].apply(normalize_name)

st.set_page_config(page_title="Times da Pelega", layout="centered")
st.image("assets/logo.png", width=200)
st.title("Times da Pelega")

# Seleção de número de times (2 ou 3)
num_teams = st.radio("Número de Equipes:", [2, 3])

st.subheader("Lista de Jogadores")
player_input = st.text_area("Cole a lista de jogadores aqui", height=200)

if st.button("FAZER TIMES"):
    if not player_input.strip():
        st.warning("Insira a lista de jogadores antes de continuar.")
    else:
        # Processar entrada e separar jogadores mensalistas e avulsos
        mensalistas, avulsos = parse_players(player_input)

        matched_players = []
        for player in mensalistas:
            normalized_player = normalize_name(player)  # Aplicar normalização antes da busca
            found = df_base[df_base["Nome"] == normalized_player]
            
            if not found.empty:
                matched_players.append(found.iloc[0].to_dict())  # Jogador encontrado no banco de dados
            else:
                # Se o jogador não estiver no banco de dados, criar uma entrada padrão
                matched_players.append({
                    "Nome": player, "Técnica": 3, "Ataque": 3, "Velocidade": 3,
                    "Físico": 3, "Defesa": 3, "Tática": 3
                })

        # Criar DataFrame com jogadores selecionados
        df_players = pd.DataFrame(matched_players)

        # Balancear os jogadores nos times
        teams = balance_teams(df_players, num_teams=num_teams)

        colors = ["red", "blue", "black"]
        image_paths = []

        for i, team in teams.items():
            team_number = i + 1

            # Calcular média dos atributos para o time
            team_data = {attr: df_players[df_players['Nome'].isin(team)][attr].mean() for attr in 
                         ["Técnica", "Ataque", "Velocidade", "Físico", "Defesa", "Tática"]}

            # Gerar e salvar gráfico de radar do time
            image_path = f"generated/team_{team_number}.png"
            create_radar_chart(team_number, team_data, image_path, color=colors[i])
            image_paths.append(image_path)

            # Exibir o gráfico no Streamlit
            st.image(image_path, caption=f"Time {team_number}", width=300)

        # Botões para baixar as imagens dos times
        st.subheader("Baixar Times")
        for image in image_paths:
            with open(image, "rb") as file:
                st.download_button(label=f"Baixar {image}", data=file, file_name=image, mime="image/png")
