import pandas as pd
from balance import balance_teams
from team_selection import calcular_diferenca_mg

# Criar uma base de jogadores fictícia para teste
data = {
    "Nome": ["Jogador1", "Jogador2", "Jogador3", "Jogador4", "Jogador5", "Jogador6"],
    "Físico": [4, 3, 5, 4, 2, 3],
    "Velocidade": [3, 4, 2, 3, 5, 4],
    "Defesa": [5, 2, 3, 4, 4, 5],
    "Tática": [3, 5, 2, 4, 3, 3],
    "Técnica": [4, 3, 4, 2, 5, 4],
    "Ataque": [2, 5, 4, 3, 3, 2],
    "Pos1": ["CB", "CM", "ST", "LB", "CM", "RW"]
}

df_players = pd.DataFrame(data)

# Testando a formação dos times com 2 times
teams = balance_teams(df_players, num_teams=2)
print("\nTimes Formados:")
for team_id, players in teams.items():
    print(f"Time {team_id+1}: {players}")

# Testando a diferença de MG entre os times
medias, diff = calcular_diferenca_mg(teams, df_players)
print("\nMédias dos Times:")
for i, media in enumerate(medias):
    print(f"Time {i+1}: {media:.3f}")

print(f"\nDiferença entre os Times: {diff:.3f}")

