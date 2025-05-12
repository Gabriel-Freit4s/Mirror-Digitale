import os
import time
import random
import pandas as pd
from datetime import datetime

def init_csv():

    if not os.path.isfile(CSV_FILE):
        df0 = pd.DataFrame(initial_data)
        df0["Data de Entrada"] = df0["Data de Entrada"].apply(parse_pt_date)
        df0.to_csv(CSV_FILE, index=False, encoding="utf-8-sig")
        print(f"[{datetime.now()}] CSV inicial criado com {len(df0)} registros.")
    else:
        print(f"[{datetime.now()}] CSV já existe. Pulando inicialização.")

def carregar_dados() -> pd.DataFrame:

    df = pd.read_csv(CSV_FILE, dtype=str)
    df["Data de Entrada"] = df["Data de Entrada"].apply(parse_mixed_date)
    df["ID"] = df["ID"].astype(int)
    df["Acuracia saude"] = df["Acuracia saude"].astype(int)
    return df

def gerar_nova_planta(df: pd.DataFrame) -> dict:
    
    next_id = df["ID"].max() + 1
    setor_let = random.choice(list(SETORES.keys()))
    nome_planta = random.choice(list(PLANTAS.keys()))
    tipo_planta = PLANTAS[nome_planta]

    return {
        "ID": next_id,
        "Nome da Planta": nome_planta,
        "Tipo de Planta": tipo_planta,
        "Saúde da Planta": random.choice(SAUDES),
        "Acuracia saude": random.randint(80, 100),
        "Data de Entrada": datetime.now(),
        "Posição de armazenagem": f"Setor {setor_let}",
        "Setor": random.choice(SETORES[setor_let]),
        "Estado Atual": random.choice(ESTADOS),
    }

def atualizar_planta(df: pd.DataFrame) -> pd.DataFrame:

    idx = random.choice(df.index)
    df.at[idx, "Saúde da Planta"] = random.choice(SAUDES)
    df.at[idx, "Acuracia saude"] = random.randint(80, 100)
    df.at[idx, "Estado Atual"] = random.choice(ESTADOS)
    return df

def main_loop():
    init_csv()
    while True:
        df = carregar_dados()
        if random.choice([True, False]):
            nova = gerar_nova_planta(df)
            df = pd.concat([df, pd.DataFrame([nova])], ignore_index=True)
            print(f"[{datetime.now()}] Novo registro ID={nova['ID']} adicionado.")
        else:
            df = atualizar_planta(df)
            print(f"[{datetime.now()}] Registro existente atualizado.")
        df.to_csv(CSV_FILE, index=False, encoding="utf-8-sig")
        time.sleep(INTERVAL_SEC)

def parse_pt_date(s: str) -> pd.Timestamp:

    d, m, y = s.split('/')
    mm = month_map[m.lower()]
    return pd.to_datetime(f"{d}/{mm}/{y}", format="%d/%m/%y")

def parse_mixed_date(s) -> pd.Timestamp:

    if isinstance(s, str) and '/' in s:
        return parse_pt_date(s)
    else:
        return pd.to_datetime(s)
    
CSV_FILE = "plantas.csv"
INTERVAL_SEC = 10

initial_data = [
    {"ID": 1,  "Nome da Planta": "Orquídea",      "Tipo de Planta": "Ornamental", "Saúde da Planta": "Boa",       "Acuracia saude": 95,  "Data de Entrada": "10/jan/24", "Posição de armazenagem": "Setor A", "Setor": "A1", "Estado Atual": "Vendida"},
    {"ID": 2,  "Nome da Planta": "Rosa",          "Tipo de Planta": "Ornamental", "Saúde da Planta": "Excelente","Acuracia saude": 96,  "Data de Entrada": "15/fev/24", "Posição de armazenagem": "Setor A", "Setor": "A2", "Estado Atual": "No Viveiro"},
    {"ID": 3,  "Nome da Planta": "Samambaia",     "Tipo de Planta": "Folhagem",   "Saúde da Planta": "Ruim",      "Acuracia saude": 99,  "Data de Entrada": "12/mar/24", "Posição de armazenagem": "Setor A", "Setor": "A3", "Estado Atual": "Morta"},
    {"ID": 4,  "Nome da Planta": "Cacto",         "Tipo de Planta": "Suculenta",  "Saúde da Planta": "Ruim",      "Acuracia saude": 94,  "Data de Entrada": "18/abr/24", "Posição de armazenagem": "Setor B", "Setor": "B1", "Estado Atual": "Danificada"},
    {"ID": 5,  "Nome da Planta": "Bromélia",      "Tipo de Planta": "Ornamental", "Saúde da Planta": "Boa",       "Acuracia saude": 98,  "Data de Entrada": "22/mai/24", "Posição de armazenagem": "Setor B", "Setor": "B2", "Estado Atual": "Vendida"},
    {"ID": 6,  "Nome da Planta": "Tulipa",        "Tipo de Planta": "Ornamental", "Saúde da Planta": "Excelente","Acuracia saude": 94,  "Data de Entrada": "30/jun/24", "Posição de armazenagem": "Setor B", "Setor": "B3", "Estado Atual": "No Viveiro"},
    {"ID": 7,  "Nome da Planta": "Jasmim",        "Tipo de Planta": "Ornamental", "Saúde da Planta": "Boa",       "Acuracia saude": 86,  "Data de Entrada": "05/jul/24", "Posição de armazenagem": "Setor C", "Setor": "C1", "Estado Atual": "No Viveiro"},
    {"ID": 8,  "Nome da Planta": "Hortênsia",     "Tipo de Planta": "Ornamental", "Saúde da Planta": "Ruim",      "Acuracia saude": 85,  "Data de Entrada": "12/ago/24", "Posição de armazenagem": "Setor C", "Setor": "C2", "Estado Atual": "Danificada"},
    {"ID": 9,  "Nome da Planta": "Girassol",      "Tipo de Planta": "Ornamental", "Saúde da Planta": "Excelente","Acuracia saude": 89,  "Data de Entrada": "20/jan/24", "Posição de armazenagem": "Setor C", "Setor": "C3", "Estado Atual": "No Viveiro"},
    {"ID": 10, "Nome da Planta": "Lavanda",       "Tipo de Planta": "Aromática",  "Saúde da Planta": "Boa",       "Acuracia saude": 91,  "Data de Entrada": "25/fev/24", "Posição de armazenagem": "Setor D", "Setor": "D1", "Estado Atual": "Vendida"},
    {"ID": 11, "Nome da Planta": "Alecrim",       "Tipo de Planta": "Aromática",  "Saúde da Planta": "Boa",       "Acuracia saude": 99,  "Data de Entrada": "05/mar/24", "Posição de armazenagem": "Setor D", "Setor": "D2", "Estado Atual": "No Viveiro"},
    {"ID": 12, "Nome da Planta": "Suculenta",     "Tipo de Planta": "Suculenta",  "Saúde da Planta": "Excelente","Acuracia saude": 88,  "Data de Entrada": "15/mar/24", "Posição de armazenagem": "Setor D", "Setor": "D3", "Estado Atual": "No Viveiro"},
    {"ID": 13, "Nome da Planta": "Begônia",       "Tipo de Planta": "Ornamental", "Saúde da Planta": "Boa",       "Acuracia saude": 86,  "Data de Entrada": "01/abr/24", "Posição de armazenagem": "Setor E", "Setor": "E1", "Estado Atual": "Vendida"},
    {"ID": 14, "Nome da Planta": "Azaleia",       "Tipo de Planta": "Ornamental", "Saúde da Planta": "Ruim",      "Acuracia saude": 91,  "Data de Entrada": "10/abr/24", "Posição de armazenagem": "Setor E", "Setor": "E2", "Estado Atual": "Morta"},
    {"ID": 15, "Nome da Planta": "Lírio",         "Tipo de Planta": "Ornamental", "Saúde da Planta": "Excelente","Acuracia saude": 85,  "Data de Entrada": "05/mai/24", "Posição de armazenagem": "Setor E", "Setor": "E3", "Estado Atual": "Vendida"},
    {"ID": 16, "Nome da Planta": "Ipê",           "Tipo de Planta": "Árvore",     "Saúde da Planta": "Boa",       "Acuracia saude": 93,  "Data de Entrada": "01/jun/24", "Posição de armazenagem": "Setor F", "Setor": "F1", "Estado Atual": "No Viveiro"},
    {"ID": 17, "Nome da Planta": "Margarida",     "Tipo de Planta": "Ornamental", "Saúde da Planta": "Boa",       "Acuracia saude": 100, "Data de Entrada": "15/jun/24", "Posição de armazenagem": "Setor F", "Setor": "F2", "Estado Atual": "No Viveiro"},
    {"ID": 18, "Nome da Planta": "Cravo",         "Tipo de Planta": "Ornamental", "Saúde da Planta": "Ruim",      "Acuracia saude": 97,  "Data de Entrada": "01/jul/24", "Posição de armazenagem": "Setor F", "Setor": "F3", "Estado Atual": "Danificada"},
    {"ID": 19, "Nome da Planta": "Bonsai",        "Tipo de Planta": "Árvore",     "Saúde da Planta": "Excelente","Acuracia saude": 96,  "Data de Entrada": "10/jul/24", "Posição de armazenagem": "Setor G", "Setor": "G1", "Estado Atual": "No Viveiro"},
    {"ID": 20, "Nome da Planta": "Violeta",       "Tipo de Planta": "Ornamental", "Saúde da Planta": "Ruim",      "Acuracia saude": 92,  "Data de Entrada": "01/ago/24", "Posição de armazenagem": "Setor G", "Setor": "G2", "Estado Atual": "Danificada"},
    {"ID": 21, "Nome da Planta": "Dália",         "Tipo de Planta": "Ornamental", "Saúde da Planta": "Boa",       "Acuracia saude": 97,  "Data de Entrada": "10/ago/24", "Posição de armazenagem": "Setor G", "Setor": "G3", "Estado Atual": "Vendida"},
    {"ID": 22, "Nome da Planta": "Crisântemo",    "Tipo de Planta": "Ornamental", "Saúde da Planta": "Excelente","Acuracia saude": 94,  "Data de Entrada": "01/set/24", "Posição de armazenagem": "Setor H", "Setor": "H1", "Estado Atual": "No Viveiro"},
    {"ID": 23, "Nome da Planta": "Camélia",       "Tipo de Planta": "Ornamental", "Saúde da Planta": "Ruim",      "Acuracia saude": 96,  "Data de Entrada": "10/set/24", "Posição de armazenagem": "Setor H", "Setor": "H2", "Estado Atual": "Morta"},
    {"ID": 24, "Nome da Planta": "Petúnia",       "Tipo de Planta": "Ornamental", "Saúde da Planta": "Excelente","Acuracia saude": 100, "Data de Entrada": "01/out/24", "Posição de armazenagem": "Setor H", "Setor": "H3", "Estado Atual": "No Viveiro"},
    {"ID": 25, "Nome da Planta": "Hibisco",       "Tipo de Planta": "Ornamental", "Saúde da Planta": "Boa",       "Acuracia saude": 90,  "Data de Entrada": "10/out/24", "Posição de armazenagem": "Setor I", "Setor": "I1", "Estado Atual": "Vendida"},
    {"ID": 26, "Nome da Planta": "Gerânio",       "Tipo de Planta": "Ornamental", "Saúde da Planta": "Boa",       "Acuracia saude": 86,  "Data de Entrada": "01/nov/24", "Posição de armazenagem": "Setor I", "Setor": "I2", "Estado Atual": "No Viveiro"},
    {"ID": 27, "Nome da Planta": "Alfazema",      "Tipo de Planta": "Aromática",  "Saúde da Planta": "Excelente","Acuracia saude": 99,  "Data de Entrada": "10/nov/24", "Posição de armazenagem": "Setor I", "Setor": "I3", "Estado Atual": "No Viveiro"},
    {"ID": 28, "Nome da Planta": "Bougainvillea", "Tipo de Planta": "Ornamental", "Saúde da Planta": "Boa",       "Acuracia saude": 97,  "Data de Entrada": "01/dez/24", "Posição de armazenagem": "Setor J", "Setor": "J1", "Estado Atual": "Danificada"},
    {"ID": 29, "Nome da Planta": "Palmeira",      "Tipo de Planta": "Árvore",     "Saúde da Planta": "Ruim",      "Acuracia saude": 100, "Data de Entrada": "10/dez/24", "Posição de armazenagem": "Setor J", "Setor": "J2", "Estado Atual": "Vendida"},
    {"ID": 30, "Nome da Planta": "Cibotium",      "Tipo de Planta": "Folhagem",   "Saúde da Planta": "Ruim",      "Acuracia saude": 91,  "Data de Entrada": "15/dez/24", "Posição de armazenagem": "Setor J", "Setor": "J3", "Estado Atual": "Danificada"},
]

month_map = {
    "jan": "01", "fev": "02", "mar": "03", "abr": "04", "mai": "05",
    "jun": "06", "jul": "07", "ago": "08", "set": "09", "out": "10",
    "nov": "11", "dez": "12"
}

nomes_das_plantas = [
    "Orquídea", "Rosa", "Samambaia", "Cacto", "Bromélia", "Tulipa", "Jasmim",
    "Hortênsia", "Girassol", "Lavanda", "Alecrim", "Suculenta", "Begônia",
    "Azaleia", "Lírio", "Ipê", "Margarida", "Cravo", "Bonsai", "Violeta",
    "Dália", "Crisântemo", "Camélia", "Petúnia", "Hibisco", "Gerânio",
    "Alfazema", "Bougainvillea", "Palmeira", "Cibotium"
]

PLANTAS ={
    "Orquídea": "Ornamental",
    "Rosa": "Ornamental",
    "Samambaia": "Folhagem",
    "Cacto": "Suculenta",
    "Bromélia": "Ornamental",
    "Tulipa": "Ornamental",
    "Jasmim": "Ornamental",
    "Hortênsia": "Ornamental",
    "Girassol": "Ornamental",
    "Lavanda": "Aromática",
    "Alecrim": "Aromática",
    "Suculenta": "Suculenta",
    "Begônia": "Ornamental",
    "Azaleia": "Ornamental",
    "Lírio": "Ornamental",
    "Ipê": "Árvore",
    "Margarida": "Ornamental",
    "Cravo": "Ornamental",
    "Bonsai": "Árvore",
    "Violeta": "Ornamental",
    "Dália": "Ornamental",
    "Crisântemo": "Ornamental",
    "Camélia": "Ornamental",
    "Petúnia": "Ornamental",
    "Hibisco": "Ornamental",
    "Gerânio": "Ornamental",
    "Alfazema": "Aromática",
    "Bougainvillea": "Ornamental",
    "Palmeira": "Árvore",
    "Cibotium": "Folhagem"
}

TIPOS = ["Ornamental", "Folhagem", "Suculenta", "Aromática", "Árvore"]
SAUDES = ["Excelente", "Boa", "Ruim"]
ESTADOS = ["Vendida", "No Viveiro", "Morta", "Danificada"]
SETORES = {
    "A": ["A1", "A2", "A3"],
    "B": ["B1", "B2", "B3"],
    "C": ["C1", "C2", "C3"],
    "D": ["D1", "D2", "D3"],
    "E": ["E1", "E2", "E3"],
    "F": ["F1", "F2", "F3"],
    "G": ["G1", "G2", "G3"],
    "H": ["H1", "H2", "H3"],
    "I": ["I1", "I2", "I3"],
    "J": ["J1", "J2", "J3"],
}

if __name__ == "__main__":
    main_loop()