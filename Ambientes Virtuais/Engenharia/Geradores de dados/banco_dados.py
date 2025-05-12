import time
import pandas as pd
import mysql.connector
import schedule
from datetime import datetime

# --- Configurações de conexão MySQL ---
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'insight-seekers',
    'password': 'diego',
    'database': 'mirror_digitale'
}

CSV_PATH = 'plantas.csv'

def atualizar_mysql():
    try:
        # 1. Lê o CSV
        df = pd.read_csv(CSV_PATH, parse_dates=['Data de Entrada'])

        # 2. Conecta ao banco
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # 3. Query corrigida com placeholders e nomes de colunas compatíveis
        sql = """
        INSERT INTO plantas (
            ID, Nome_da_Planta, Tipo_de_Planta, Saude_da_Planta,
            Acuracia_saude, Data_de_Entrada, Posicao_de_armazenagem,
            Setor, Estado_Atual
        ) VALUES (
            %(ID)s, %(Nome_da_Planta)s, %(Tipo_de_Planta)s, %(Saude_da_Planta)s,
            %(Acuracia_saude)s, %(Data_de_Entrada)s, %(Posicao_de_armazenagem)s,
            %(Setor)s, %(Estado_Atual)s
        )
        ON DUPLICATE KEY UPDATE
            Nome_da_Planta = VALUES(Nome_da_Planta),
            Tipo_de_Planta = VALUES(Tipo_de_Planta),
            Saude_da_Planta = VALUES(Saude_da_Planta),
            Acuracia_saude = VALUES(Acuracia_saude),
            Data_de_Entrada = VALUES(Data_de_Entrada),
            Posicao_de_armazenagem = VALUES(Posicao_de_armazenagem),
            Setor = VALUES(Setor),
            Estado_Atual = VALUES(Estado_Atual);
        """

        # 4. Mapeamento corrigido dos nomes das colunas
        for row in df.to_dict(orient='records'):
            params = {
                'ID': row['ID'],
                'Nome_da_Planta': row['Nome da Planta'],
                'Tipo_de_Planta': row['Tipo de Planta'],
                'Saude_da_Planta': row['Saúde da Planta'],
                'Acuracia_saude': row['Acuracia saude'],
                'Data_de_Entrada': row['Data de Entrada'].to_pydatetime(),
                'Posicao_de_armazenagem': row['Posição de armazenagem'],
                'Setor': row['Setor'],
                'Estado_Atual': row['Estado Atual']
            }
            cursor.execute(sql, params)

        conn.commit()
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Atualização concluída com sucesso. Registros afetados: {len(df)}")

    except mysql.connector.Error as err:
        print(f"Erro MySQL: {err}")
    except Exception as e:
        print(f"Erro inesperado: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

# --- Configuração do agendador ---
schedule.every(1).minutes.do(atualizar_mysql)

if __name__ == "__main__":
    print("Serviço de sincronização MySQL-CSV iniciado...")
    atualizar_mysql()  # Execução inicial
    
    while True:
        schedule.run_pending()
        time.sleep(1)