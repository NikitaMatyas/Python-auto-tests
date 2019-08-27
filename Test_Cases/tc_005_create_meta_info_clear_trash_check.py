from business_layer.yandex.yandex_requests import *
from framework_core.variables import disk_url, token


def test_tc_005():
    """ Создать папки test->foo и файл внутри, сравнить тип параметров, удалить данные и проверить, что они удалены
    1. Создание папки test(Код ответа == 201)
    2. Создание папки foo внутри папки test (Код ответа == 201)
    3. Получение URL для загрузки файла в папку test (Код ответа == 200, URL для загрузки)
    4. Загрузка файла по сгенерированному URL (Код ответа == 201)
    5. Получение данных о Яндекс диске и проверка типов (Код ответа == 200, типы совпадают)
    6. Удаление папки test со всеми вложенными ресурсами (Код ответа == 204 или 200)
    7. Проверка, что папка test была удалена (Код ответа == 404)
    """
    path = '%2Ftest'
    path_2 = '%2Ftest%2Ffoo'
    path_3 = '%2Ftest%2Ffoo%2Fautotest'

    data = create_folder(disk_url, token, path)
    assert data.status_code == 201, 'Не удалось создать папку на Яндекс диске'

    data = create_folder(disk_url, token, path_2)
    assert data.status_code == 201, 'Не удалось создать папку на Яндекс диске'

    data, url = file_upload_link(disk_url, token, path_3)
    assert data.status_code == 200, 'Не удалось получить URL для загрузки файла на Яндекс диск'

    data = file_upload(url)
    assert data.status_code == 201, 'Не удалось загрузить файл по сгенерированному URL'

    data = check_resource(disk_url, token, path)
    assert data.status_code == 200, 'Не удалось получить данные о Яндекс диске'
    assert data.json()["type"] == "dir"
    assert data.json()["_embedded"]["items"][0]["type"] == "dir"

    data = delete_resource(disk_url, token, path, 'true', 5)
    assert data == 204 or data == 200

    data = check_resource(disk_url, token, path)
    assert data.status_code == 404, 'Папка существует на диске или не удалось получить данные'
