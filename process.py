import unicodedata
import re

def normalize_name(name):
    """Remove acentos, caracteres especiais e padroniza o nome para comparação."""
    name = unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode('utf-8')
    name = re.sub(r'[^a-zA-Z0-9 ]', '', name)  # Remove caracteres especiais
    name = name.lower().strip()  # Converte para minúsculas
    return name

def parse_players(text):
    """
    Processa o texto de entrada para separar os jogadores mensalistas e avulsos.

    Retorna:
    - Lista de jogadores mensalistas (normalizados)
    - Lista de jogadores avulsos (normalizados)
    """
    lines = text.split("\n")
    mensalistas = []
    avulsos = []
    section = None

    for line in lines:
        line = line.strip()
        if not line:
            continue  # Ignorar linhas vazias

        if "ATLETAS MENSALISTAS" in line.upper():
            section = "mensalistas"
            continue
        elif "AVULSOS" in line.upper():
            section = "avulsos"
            continue

        if section == "mensalistas" or section == "avulsos":
            match = re.match(r"\d+\-\s*(.+)", line)  # Pega o nome após o número e "-"
            if match:
                name = match.group(1)
                normalized_name = normalize_name(name)

                if section == "mensalistas":
                    mensalistas.append(normalized_name)
                else:
                    avulsos.append(normalized_name)

    return mensalistas, avulsos
