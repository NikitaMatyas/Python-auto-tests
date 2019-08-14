from business_layer.yandex.yandex_requests import *
from framework_core.variables import disk_url, token


def test_uid():
    """ Проверка указанного id пользователя
    1. Получение информации о Яндекс Диске (Данные о диске в теле ответа)
    2. Проверка на успешное получение данных(Код ответа = 200)
    3. Проверка на соответствие id пользователя указанному (uid == user_id)
    """
    user_id = '860094785'
    data = get_disk_info(disk_url, token)
    assert data.status_code == 200, 'Не удалось получить данные о диске'
    assert data.json()["user"]["uid"] == user_id, 'Указанный id не найден'


def test_create_folder():
    """ Создание папки на Яндекс диске
    1. PUT запрос на создание папки на Яндекс диске по указанному пути(Ссылка на мета-информацию о созданной папке)
    2. Проверка на успешное создание папки (Код ответа = 201)
    """
    data = create_folder(disk_url, token, '%2FMusic')
    assert data.status_code == 201, 'Не удалось создать папку на Яндекс диске'


def test_delete_folder():
    """ Удаление папки на Яндекс диске
    1. DELETE запрос на удаление папки на Яндекс диске по указанному пути (Код ответа без тела ответа)
    2. Проверка на успешное удаление папки (Код ответа = 204)
    """
    data = delete_resource(disk_url, token, '%2FMusic', 'true', 5)
    assert data.status_code == 204 or data.status_code == 200, 'Не удалось удалить папку на Яндекс диске'


def test_check_folder_exists():
    """ Проверка существования папки на Яндекс диске
    1. GET запрос на получение мета-информации о папке (Мета-информация о запрошенной папке)
    2. Проверка на существование папки (Код ответа = 200)
    """
    data = check_folder(disk_url, token, '%2FMusic')
    assert data.status_code == 200, 'Папка не существует или не удалось получить данные'


def test_check_folder_deleted():
    """ Проверка отсутствия папки на Яндекс диске
    1. GET запрос на получение мета-информации о папке (Мета-информация о запрошенной папке)
    2. Проверка на отсутствие папки (Код ответа = 404)
    """
    data = check_folder(disk_url, token, '%2FMusic')
    assert data.status_code == 404, 'Папка существует на диске или не удалось получить данные'
