import itertools
import random
import numpy as np
import pandas as pd

import numpy as np
import pandas as pd

# Função para calcular a MG (média geral ponderada) de um jogador
def calcular_mg_jogador(row):
    return (
        row['Físico'] * 0.4 +
        row['Velocidade'] * 0.2 +
        row['Defesa'] * 0.1 +
        row['Tática'] * 0.05 +
        row['Técnica'] * 0.05 +
        row['Ataque'] * 0.1
    )

# Função para calcular a MG média de um time
def calcular_media_mg_time(df_players, team):
    """Calcula a média MG do time com base nos jogadores atribuídos."""
    df_team = df_players[df_players["Nome"].isin(team)]
    return df_team.apply(calcular_mg_jogador, axis=1).mean()

# Função para calcular a diferença entre as médias dos times
def calcular_diferenca_mg(teams, df_players):
    """Calcula a diferença entre os times baseada na média MG."""
    medias = [calcular_media_mg_time(df_players, team) for team in teams.values()]

    if len(medias) == 2:
        diff = abs(medias[0] - medias[1])
    elif len(medias) == 3:
        diff = np.sqrt(
            (abs(medias[0] - medias[1]) ** 2) +
            (abs(medias[0] - medias[2]) ** 2) +
            (abs(medias[1] - medias[2]) ** 2)
        )
    else:
        raise ValueError("Apenas suportado para 2 ou 3 times.")

    return medias, diff


# # Função para calcular o desvio padrão normalizado da MG de um time
# def calcular_desvio_mg_time(df):
#     mg_jogadores = df.apply(calcular_mg_jogador, axis=1)
#     return mg_jogadores.std() / np.sqrt(len(mg_jogadores))

# Função para contar os jogadores por categoria (usando a coluna 'Categoria')
def contar_jogadores(df):
    return df['Categoria'].value_counts().to_dict()

# Função principal para montar os times de forma balanceada
def montar_times_unicos_mg(df, n_defesa, n_meia, n_ataque):
    defensores = [f"{row['Posição']}-{row['Nome']}" for _, row in df[df['Categoria'] == 'Defesa'].iterrows()]
    meias = [f"{row['Posição']}-{row['Nome']}" for _, row in df[df['Categoria'] == 'Meia'].iterrows()]
    atacantes = [f"{row['Posição']}-{row['Nome']}" for _, row in df[df['Categoria'] == 'Atacante'].iterrows()]

    total_combinacoes = 0
    combinacoes_unicas = []
    combinacoes_vistas = set()

    # Geração de combinações para os jogadores de cada posição
    for num_def_a in range(n_defesa // 2, (n_defesa + 1) // 2 + 1):
        combinacoes_def = list(itertools.combinations(defensores, num_def_a))
        for comb_def in combinacoes_def:
            for num_meia_a in range(n_meia // 2, (n_meia + 1) // 2 + 1):
                combinacoes_meia = list(itertools.combinations(meias, num_meia_a))
                for comb_meia in combinacoes_meia:
                    for num_ataque_a in range(n_ataque // 2, (n_ataque + 1) // 2 + 1):
                        combinacoes_ataque = list(itertools.combinations(atacantes, num_ataque_a))
                        for comb_ataque in combinacoes_ataque:
                            time_a = list(comb_def) + list(comb_meia) + list(comb_ataque)
                            time_b = [jog for jog in (defensores + meias + atacantes) if jog not in time_a]

                            total_combinacoes += 1

                            if abs(len(time_a) - len(time_b)) <= 1:
                                time_a_sorted = tuple(sorted(time_a))
                                time_b_sorted = tuple(sorted(time_b))
                                if (time_a_sorted, time_b_sorted) not in combinacoes_vistas:
                                    combinacoes_vistas.add((time_a_sorted, time_b_sorted))
                                    combinacoes_unicas.append((time_a, time_b))
                                    
    print(f"Total de combinações geradas (incluindo espelhos): {total_combinacoes}")
    print(f"Total de combinações únicas (apenas espelhos removidos): {len(combinacoes_unicas)}")

    # Filtro 1 - Diferença de Média de MG
    combinacoes_filtradas_mg = [
        (time_a, time_b, abs(
            calcular_media_mg_time(df[df['Nome'].isin([jog.split('-')[1] for jog in time_a])]) -
            calcular_media_mg_time(df[df['Nome'].isin([jog.split('-')[1] for jog in time_b])])
        ))
        for time_a, time_b in combinacoes_unicas
    ]
    combinacoes_filtradas_mg = sorted(combinacoes_filtradas_mg, key=lambda x: x[2])
    limite_mg = max(1, int(len(combinacoes_filtradas_mg) * 0.20))
    combinacoes_filtradas_2 = combinacoes_filtradas_mg[:limite_mg]
    print(f"Filtro 1 - média MG (20% menor): {len(combinacoes_filtradas_2)}")

    # Filtro 2 - Diferença de Desvio Padrão da MG
    combinacoes_filtradas_desvio = [
        (time_a, time_b, abs(
            calcular_desvio_mg_time(df[df['Nome'].isin([jog.split('-')[1] for jog in time_a])]) -
            calcular_desvio_mg_time(df[df['Nome'].isin([jog.split('-')[1] for jog in time_b])])
        ))
        for time_a, time_b, _ in combinacoes_filtradas_2
    ]
    combinacoes_filtradas_desvio = sorted(combinacoes_filtradas_desvio, key=lambda x: x[2])
    limite_desvio = max(1, int(len(combinacoes_filtradas_desvio) * 0.20))
    combinacoes_finais = combinacoes_filtradas_desvio[:limite_desvio]
    print(f"Filtro 2 - desvio MG (20% menor): {len(combinacoes_finais)}")

    # Filtro 3 - Diferença de Defesa
    combinacoes_filtradas_defesa = [
        (time_a, time_b, abs(
            df[df['Nome'].isin([jog.split('-')[1] for jog in time_a])]['Defesa'].mean() -
            df[df['Nome'].isin([jog.split('-')[1] for jog in time_b])]['Defesa'].mean()
        ))
        for time_a, time_b, _ in combinacoes_finais
    ]
    combinacoes_filtradas_defesa = sorted(combinacoes_filtradas_defesa, key=lambda x: x[2])
    limite_defesa = max(1, int(len(combinacoes_filtradas_defesa) * 0.20))
    combinacoes_finais_defesa = combinacoes_filtradas_defesa[:limite_defesa]
    print(f"Filtro 3 - Defesa (20% menor): {len(combinacoes_finais_defesa)}")

    # Filtro 4 - Diferença de Ataque
    combinacoes_filtradas_ataque = [
        (time_a, time_b, abs(
            df[df['Nome'].isin([jog.split('-')[1] for jog in time_a])]['Ataque'].mean() -
            df[df['Nome'].isin([jog.split('-')[1] for jog in time_b])]['Ataque'].mean()
        ))
        for time_a, time_b, _ in combinacoes_finais_defesa
    ]
    combinacoes_filtradas_ataque = sorted(combinacoes_filtradas_ataque, key=lambda x: x[2])
    limite_ataque = max(1, int(len(combinacoes_filtradas_ataque) * 0.20))
    combinacoes_finais_ataque = combinacoes_filtradas_ataque[:limite_ataque]
    print(f"Filtro 4 - Ataque (20% menor): {len(combinacoes_finais_ataque)}")

    # Filtro 5 - Diferença de Técnica
    combinacoes_filtradas_tecnica = [
        (time_a, time_b, abs(
            df[df['Nome'].isin([jog.split('-')[1] for jog in time_a])]['Técnica'].mean() -
            df[df['Nome'].isin([jog.split('-')[1] for jog in time_b])]['Técnica'].mean()
        ))
        for time_a, time_b, _ in combinacoes_finais_ataque
    ]
    combinacoes_filtradas_tecnica = sorted(combinacoes_filtradas_tecnica, key=lambda x: x[2])
    limite_tecnica = max(1, int(len(combinacoes_filtradas_tecnica) * 0.20))
    combinacoes_finais_tecnica = combinacoes_filtradas_tecnica[:limite_tecnica]
    print(f"Filtro 5 - Técnica (20% menor): {len(combinacoes_finais_tecnica)}")

    # Seleção final: caso haja mais de uma opção, escolhe aleatoriamente
    if len(combinacoes_finais_tecnica) > 1:
        time_a, time_b, _ = random.choice(combinacoes_finais_tecnica)
    else:
        time_a, time_b, _ = combinacoes_finais_tecnica[0]

    # Organização dos jogadores por posição
    ordem_posicoes = ['CB', 'LB', 'RB', 'CDM', 'CM', 'CAM', 'LM', 'RM', 'LW', 'RW', 'ST']
    time_a_sorted = sorted(time_a, key=lambda x: ordem_posicoes.index(x.split("-")[0])
                          if x.split("-")[0] in ordem_posicoes else len(ordem_posicoes))
    time_b_sorted = sorted(time_b, key=lambda x: ordem_posicoes.index(x.split("-")[0])
                          if x.split("-")[0] in ordem_posicoes else len(ordem_posicoes))
    
    print("\nTime A vs Time B:")
    max_len = max(len(time_a_sorted), len(time_b_sorted))
    for i in range(max_len):
        jogador_a = time_a_sorted[i] if i < len(time_a_sorted) else ""
        jogador_b = time_b_sorted[i] if i < len(time_b_sorted) else ""
        print(f"{jogador_a:<20} | {jogador_b:<20}")
    
    return time_a_sorted, time_b_sorted
