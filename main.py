from flask import Flask
import sqlite3 as lite


dias = ['um', 'dois', 'tres', 'quatro', 'cinco', 'seis', 'sete', 'oito',
        'novo', 'dez', 'onze', 'doze', 'treze', 'quatorze', 'quinze',
        'dezesseis', 'dezessete', 'dezoito', 'dezenove', 'vinte', 'vinte_e_um',
        'vinte_e_dois', 'vinte_e_três']

datas = ['20', '21', '22', '23', '24', '25', '26', '27', '28', '29',
         '30', '01', '02', '03', '04', '05', '06', '09', '10', '13',
         '14', '17', '18']

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
    dia = data[:2]
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
