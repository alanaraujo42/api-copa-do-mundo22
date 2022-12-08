from datetime import datetime
from time import sleep
from login.login_api import login_api_wc22
import pytz
import requests
import sqlite3 as lite

dias_extenso = ['um', 'dois', 'tres', 'quatro', 'cinco', 'seis', 'sete', 'oito', 'novo',
                'dez', 'onze', 'doze', 'treze', 'quatorze', 'quinze', 'dezesseis',
                'dezessete', 'dezoito', 'dezenove', 'vinte', 'vinte_e_um',
                'vinte_e_dois', 'vinte_e_três']

data = ['20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30',
        '01', '02', '03', '04', '05', '06', '09', '10', '13', '14', '17',
        '18']

dic = zip(data, dias_extenso)
dic = dict(dic)

dias_numero = [i for i in range(1, 24)]
dias_partida = zip(data, dias_numero)
dias_partida = dict(dias_partida)

fuso_BR = pytz.timezone('Brazil/East')

while True:
    # Obter o dia atual
    horario_BR = datetime.now(fuso_BR)
    dia = horario_BR.strftime('%d')
    # Verificar se o dia atual passou do dia 18/12 (fim da copa)
    if int(dia) > 18:
        # Se sim - Break no Código
        break
    # Se não - Realizar UPDATE no DB a cada 1:30h
    else:
        # Pegar do dicionário, o nome por escrito, para atualizar a tabela daquele dia
        if dia not in dic:
            pass
        else:
            nome_tabela = dic[dia]
            dia_p = str(dias_partida[dia])
            # Após isso, rodar o código de UPDATE do DB
            # Definido informações para GET
            token = login_api_wc22()
            # Utilizar dia para parametrô de requisição no link do get
            link = f'http://api.cup2022.ir/api/v1/bymatch/{dia_p}'
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
                time_1_jogadores_gol = str(parti['home_scorers'])
                time_1_jogadores_gol = time_1_jogadores_gol.replace("'", '')
                time_2_jogadores_gol = str(parti['away_scorers'])
                time_2_jogadores_gol = time_2_jogadores_gol.replace("'", '')
                placar_final = f"""{parti['home_team_en']} {parti['home_score']} X
{parti['away_team_en']} {parti['away_score']}"""
                # Valores para ser usado no comando do SQL
                valores = [parti['home_score'], time_1_jogadores_gol, parti['away_score'],
                           time_2_jogadores_gol, parti['finished'], placar_final,
                           parti['id']]
                comando = f"""
            UPDATE dia_{nome_tabela}
            SET time_1_qtd_gol = ?, time_1_jogadores_gol = ?, time_2_qtd_gol = ?,
            time_2_jogadores_gol = ?, jogo_finalizado = ?, placar_final = ?
            WHERE id_partida = ?"""
                # Executando comando SQL no DB
                cursor.execute(comando, valores)
                conn.commit()
    # Depois, realizar um Sleep para esperar 1:30h para atualizar novamente
    sleep(5400)
