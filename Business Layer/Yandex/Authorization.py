import requests
import json

headers = {'response_type': 'token', 'client_id': '21f1d80a84bc4d5d9a1aee802e62e6b4'}
r = requests.post('https://oauth.yandex.ru/authorize', headers=headers)
print(r.text)

'''
Из этой херни нужно вытянуть токен, https://yandex.ru/dev/oauth/doc/dg/reference/web-client-docpage/ 
Данные о токене передаются в URL перенаправления после символа #
'''

