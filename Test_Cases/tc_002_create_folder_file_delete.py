from business_layer.yandex.yandex_requests import *
from framework_core.variables import disk_url, token


def test_create_delete_check():
    """ Создание папки на Яндекс Диске, создание файла внутри папки, удаление файла и папки
    1. PUT запрос на создание папки по указанному пути (Ссылка на мета-информацию о созданной папке)
    2. Проверка на успешное создание папки (Код ответа = 201)
    3. Генерация URL адреса для загрузки файла на Яндекс диск (Ссылка для загрузки файла)
    4. Проверка на успешную генерацию URL адреса (Код ответа = 200)
    5. PUT запрос на создание файла в папке на Яндекс диске по указанному пути (Ссылка на мета-информацию о файле)
    6. Проверка на успешное создание файла (Код ответа == 201)
    7. DELETE запрос на удаление файла в папке на Яндекс диске по указанному пути (Код ответа без тела ответа)
    8. Проверка на успешное удаление файла (Код ответа == 204)
    9. DELETE запрос на удаление папки на Яндекс диске по указанному пути (Код ответа без тела ответа)
    10. Проверка на успешное удаление папки (Код ответа == 204)
    """
    path = '%2FMusic'
    path_2 = '%2FMusic%2FSong.txt'

    data = create_folder(disk_url, token, path)
    assert data.status_code == 201, 'Не удалось создать папку на Яндекс диске'

    data, url = file_upload_link(disk_url, token, path_2)
    assert data.status_code == 200, 'Не удалось получить URL для загрузки файла на Яндекс диск'

    data = file_upload(url)
    assert data.status_code == 201, 'Не удалось загрузить файл по сгенерированному URL'

    data = delete_resource(disk_url, token, path_2, 'true', 5)
    assert data.status_code == 204 or data.status_code == 200, 'Не удалось удалить файл в папке на Яндекс диске'

    data = delete_resource(disk_url, token, path, 'true', 5)
    assert data.status_code == 204 or data.status_code == 200, 'Не удалось удалить папку на Яндекс диске'
