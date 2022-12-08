import requests
import sqlite3 as lite
from login.login_api import login_api_wc22

dias_extenso = ['um', 'dois', 'tres', 'quatro', 'cinco', 'seis', 'sete',
                'oito', 'novo', 'dez', 'onze', 'doze', 'treze', 'quatorze',
                'quinze', 'dezesseis', 'dezessete', 'dezoito', 'dezenove',
                'vinte', 'vinte_e_um', 'vinte_e_dois', 'vinte_e_três']

token = login_api_wc22()

n = 1
for dia in dias_extenso:
    # Definido informações para GET
    link = f'http://api.cup2022.ir/api/v1/bymatch/{n}'
    header = {
        'Authorization':  token,
        'Content-Type': 'application/json'
    }

    # Realizando requisição
    resultado = requests.get(url=link, headers=header)
    # Dado obtido
    resultado_dic = resultado.json()
    partida = resultado_dic['data']
    # Conectando com bano de dados
    conn = lite.connect('dados_partidas_wc22.db')
    cursor = conn.cursor()
    # For para pegar as informações das partidas do dia
    for parti in partida:
        # Definindo variáveis para colocar no DB
        time_1_jogadores_gol = str(parti['home_scorers'])
        time_1_jogadores_gol = time_1_jogadores_gol.replace("'", '')
        time_2_jogadores_gol = str(parti['away_scorers'])
        time_2_jogadores_gol = time_2_jogadores_gol.replace("'", '')
        placar_final = f"""{parti['home_team_en']} {parti['home_score']} X
{parti['away_team_en']} {parti['away_score']}"""
        # Criando lista de valores para colocar no camdando do SQLite
        valores = [parti['id'], parti['home_team_en'], parti['home_score'],
                   time_1_jogadores_gol, parti['away_team_en'],
                   parti['away_score'], time_2_jogadores_gol, parti['group'],
                   parti['type'], parti['finished'], placar_final]
        # Comando SQL
        comando = f"""INSERT INTO dia_{dia}
    (id_partida, time_1, time_1_qtd_gol, time_1_jogadores_gol, time_2,
    time_2_qtd_gol, time_2_jogadores_gol, grupo_do_time,
    tipo_de_partida, jogo_finalizado, placar_final)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        # Executando o camando SQLite para o DB
        cursor.execute(comando, valores)
        conn.commit()
    n += 1
