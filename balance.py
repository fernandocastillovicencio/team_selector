import random
import pandas as pd

def balance_teams(df_players, num_teams=2):
    """
    Balanceia os jogadores em times de maneira equitativa.

    Parâmetros:
    - df_players: DataFrame contendo os jogadores e seus atributos
    - num_teams: Número de times a serem formados

    Retorna:
    - Dicionário com a lista de jogadores para cada time
    """
    players_list = df_players["Nome"].tolist()
    random.shuffle(players_list)  # Embaralha os jogadores

    teams = {i: [] for i in range(num_teams)}
    
    for i, player in enumerate(players_list):
        team_index = i % num_teams
        teams[team_index].append(player)
    
    return teams
