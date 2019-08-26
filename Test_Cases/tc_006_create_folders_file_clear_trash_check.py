from business_layer.yandex.yandex_requests import *
from framework_core.variables import disk_url, token


def test_tc_006():
    """ Создать папки test->foo и файл внутри, очистить корзину и проверить, что корзина очищена
    1. Создание папки test на Яндекс диске (Код ответа == 201)
    2. Создание папки foo внутри папки test (Код ответа == 201)
    3. Получение URL для загрузки файла в папку test (Код ответа == 200, URL для загрузки)
    4. Загрузка файла по сгенерированному URL (Код ответа == 201)
    5. Помещение папки test в корзину (Код ответа == 204 или 200)
    6. Очистка корзины (Код ответа == 204 или 200)
    """
    data = create_folder(disk_url, token, '%2Ftest')
    assert data.status_code == 201, 'Не удалось создать папку на Яндекс диске'

    data = create_folder(disk_url, token, '%2Ftest%2Ffoo')
    assert data.status_code == 201, 'Не удалось создать папку на Яндекс диске'

    data, url = file_upload_link(disk_url, token, '%2Ftest%2Ffoo%2Fautotest')
    assert data.status_code == 200, 'Не удалось получить URL для загрузки файла на Яндекс диск'

    data = file_upload(url)
    assert data.status_code == 201, 'Не удалось загрузить файл по сгенерированному URL'

    data = delete_resource(disk_url, token, '%2Ftest', 'false', 1)
    assert data == 204 or data == 200

    data = clear_trash(disk_url, token, '%2Ftest', 1)
    assert data == 204 or data == 200
