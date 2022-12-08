import requests
import json


def login_api_wc22():
    link = 'http://api.cup2022.ir/api/v1/user/login'
    header = {'Content-Type': 'application/json'}
    data_raw = {
        "email": "alanaraujodev0@gmail.com",
        "password": "copadomundo@123"
    }

    resultado = requests.post(url=link, headers=header,
                              data=json.dumps(data_raw))
    resultado_dic = resultado.json()
    token_login = resultado_dic['data']['token']
    return token_login
