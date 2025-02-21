import streamlit as st
import pandas as pd
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

        # 🔹 Exibir os resultados no Streamlit
        st.subheader("Jogadores reconhecidos na base de dados:")
        st.write([p["Nome"] for p in matched_players if p["Nome"] not in unrecognized_players])

        st.subheader("Jogadores não reconhecidos (completados com CM e nota 3):")
        st.write(unrecognized_players)

        # 🔹 Balancear os jogadores nos times
        teams = balance_teams(pd.DataFrame(matched_players), num_teams=num_teams)

        # 🔹 Calcular diferença de MG entre os times
        medias, diff = calcular_diferenca_mg(teams, pd.DataFrame(matched_players))

        # 🔹 Exibir médias de cada time
        st.subheader("Médias Ponderadas dos Times:")
        for i, media in enumerate(medias):
            st.write(f"**Time {i+1}:** {media:.3f}")

        # 🔹 Exibir diferença entre os times
        st.subheader("Diferença entre as Médias dos Times:")
        st.write(f"**Diferença Total:** {diff:.3f}")

        # 🔹 Gerar e salvar gráficos radar dos times
        colors = ["red", "blue", "black"]
        image_paths = []
        team_lists = []

        for i, team in teams.items():
            team_number = i + 1

            # 🔹 Calcular média dos atributos para o time
            team_data = {attr: pd.DataFrame(matched_players)[pd.DataFrame(matched_players)['Nome'].isin(team)][attr].mean() 
                         for attr in ["Técnica", "Ataque", "Velocidade", "Físico", "Defesa", "Tática"]}

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
        st.image(combined_image_path, caption="Times Formados", width=900)

        # 🔹 Botão para baixar a imagem final
        with open(combined_image_path, "rb") as file:
            st.download_button(label="Baixar Imagem dos Times", data=file, file_name="times_combinados.png", mime="image/png")
