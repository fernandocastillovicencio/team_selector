import random
import pandas as pd

import random
import pandas as pd

def balance_teams(df_players, num_teams=2):
    """
    Balanceia os jogadores em times de maneira equitativa, garantindo separação
    entre zagueiros, meias e atacantes e mantendo a ordem de distribuição.

    Parâmetros:
    - df_players: DataFrame contendo os jogadores e seus atributos.
    - num_teams: Número de times a serem formados.

    Retorna:
    - Dicionário com a lista de jogadores para cada time.
    """

    # Separar os jogadores por posição
    defenders = df_players[df_players["Pos1"].isin(["CB", "LB", "RB"])].sample(frac=1).to_dict(orient="records")
    midfielders = df_players[df_players["Pos1"].isin(["CM", "CDM", "CAM", "LM", "RM"])].sample(frac=1).to_dict(orient="records")
    attackers = df_players[df_players["Pos1"].isin(["ST", "LW", "RW"])].sample(frac=1).to_dict(orient="records")

    teams = {i: [] for i in range(num_teams)}

    def distribute_players(players, start_team):
        """Distribui jogadores em times na ordem ABC ou AB."""
        for i, player in enumerate(players):
            team_index = (start_team + i) % num_teams
            teams[team_index].append(player)

    # Distribuição dos zagueiros
    distribute_players(defenders, start_team=0)

    # Descobrir onde o último zagueiro foi colocado
    last_team_index = (len(defenders) - 1) % num_teams

    # Distribuição dos meias
    distribute_players(midfielders, start_team=(last_team_index + 1) % num_teams)

    # Descobrir onde o último meia foi colocado
    last_team_index = (last_team_index + len(midfielders)) % num_teams

    # Distribuição dos atacantes
    distribute_players(attackers, start_team=(last_team_index + 1) % num_teams)

    # Transformar times em formato apenas com nomes para retorno
    teams = {key: [player["Nome"] for player in value] for key, value in teams.items()}

    return teams

