import requests
import json
from BusinessLayer.Yandex import Authorization


def get_disk_info():
    headers = {'Authorization': Authorization.get_token()}
    r = requests.get('https://cloud-api.yandex.net/v1/disk/', headers=headers)
    print(json.dumps(r.json(), indent=4))


get_disk_info()
