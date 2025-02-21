from radar_chart import create_radar_chart
from combine_images import create_combined_image

# Gerar gráficos radar para cada time
image_paths = []
fig_size = 520
colors = ["red", "blue"]

for i, team in teams.items():
    team_data = {attr: df_players[df_players['Nome'].isin(team)][attr].mean() 
                 for attr in ["Físico", "Defesa", "Tática", "Técnica", "Ataque", "Velocidade"]}

    image_path = f"generated/team_{i+1}.png"
    create_radar_chart(i+1, team_data, image_path, colors[i])
    image_paths.append(image_path)

# Criar a imagem combinada
combined_image_path = "generated/combined_teams_test.png"
create_combined_image(image_paths, list(teams.values()), combined_image_path, fig_size)

print(f"\nImagem combinada salva em: {combined_image_path}")
