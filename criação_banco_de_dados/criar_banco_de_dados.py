import sqlite3 as lite


dias = ['um', 'dois', 'tres', 'quatro', 'cinco', 'seis', 'sete', 'oito',
        'novo', 'dez', 'onze', 'doze', 'treze', 'quatorze', 'quinze',
        'dezesseis', 'dezessete', 'dezoito', 'dezenove',
        'vinte', 'vinte_e_um', 'vinte_e_dois', 'vinte_e_três']
data = ['20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '01',
        '02', '03', '04', '05', '06', '09', '10', '13', '14', '17', '18']
dic = zip(dias, data)
dic = dict(dic)


conn = lite.connect('dados_partidas_wc22.db')
cursor = conn.cursor()
n = 20
m = '11'
for k, v in dic.items():
    if n > 30:
        m = '12'
    comando = f"""CREATE TABLE IF NOT EXISTS dia_{k}(
    id_partida text,
    dia DEFAULT('{v}/{m}/22'),
    time_1 text,
    time_1_qtd_gol text,
    time_1_jogadores_gol text,
    time_2 text,
    time_2_qtd_gol text,
    time_2_jogadores_gol text,
    grupo_do_time text,
    tipo_de_partida text,
    jogo_finalizado text,
    placar_final text
  )"""
    cursor.execute(comando)
    n += 1
