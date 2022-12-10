from flask import Flask
import sqlite3 as lite


dias = ['um', 'dois', 'tres', 'quatro', 'cinco', 'seis', 'sete', 'oito',
        'novo', 'dez', 'onze', 'doze', 'treze', 'quatorze', 'quinze',
        'dezesseis', 'dezessete', 'dezoito', 'dezenove', 'vinte', 'vinte_e_um',
        'vinte_e_dois', 'vinte_e_três']

datas = ['2011', '2111', '2211', '2311', '2411', '2511', '2611', '2711', '2811', '2911',
         '3011', '0112', '0212', '0312', '0412', '0512', '0612', '0912', '1012', '1312',
         '1412', '1712', '1812']

legendas = ['id_partida', 'dia', 'time_1', 'time_1_qtd_gol', 'time_1_jogadores_gol',
            'time_2', 'time_2_qtd_gol', 'time_2_jogadores_gol',
            'grupo_do_time', 'tipo_de_partida', 'jogo_finalizado',
            'placar_final']

dic = zip(datas, dias)
dic = dict(dic)

conn = lite.connect('dados_partidas_wc22.db')
cursor = conn.cursor()

app = Flask(__name__)  # Cria o Site


@app.route("/partida/<data>")
def partida_dia(data):  # Função
    dia = data[:4]
    if dia in datas:
        tabela = dic[dia]
        conn = lite.connect('dados_partidas_wc22.db')
        cursor = conn.cursor()
        comando = f"SELECT * FROM dia_{tabela}"
        cursor.execute(comando)
        resultado = cursor.fetchall()
        lista = []
        for partida in resultado:
            dicionario = zip(legendas, partida)
            dicionario = dict(dicionario)
            lista.append(dicionario)
        return {'Menssagem': 'Sucesso', 'dados': lista}
    else:
        return {'Menssagem': 'Erro', 'dados': 'Nesta data não tem jogos'}


app.run()  # Coloca o site no ar
