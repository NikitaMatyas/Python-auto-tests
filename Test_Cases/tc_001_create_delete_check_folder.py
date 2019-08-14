from business_layer.yandex.yandex_requests import *
from framework_core.variables import disk_url, token


def test_create_delete_check():
    """ Создание папки на Яндекс Диске, удаление папки и проверка, что папка была удалена
    1. PUT запрос на создание папки на Яндекс диске по указанному пути(Ссылка на мета-информацию о созданной папке)
    2. Проверка на успешное создание папки (Код ответа = 201)
    3. DELETE запрос на удаление папки на Яндекс диске по указанному пути (Код ответа без тела ответа)
    4. Проверка на успешное удаление папки (Код ответа = 204)
    5. GET запрос на получение мета-информации о папке (Мета-информация о запрошенной папке)
    6. Проверка на отсутствие папки (Код ответа = 404)
    """
    data = create_folder(disk_url, token, '%2FMusic')
    assert data.status_code == 201, 'Не удалось создать папку на Яндекс диске'

    data = delete_resource(disk_url, token, '%2FMusic', 'true', 5)
    assert data.status_code == 204 or data.status_code == 200, 'Не удалось удалить папку на Яндекс диске'

    data = check_folder(disk_url, token, '%2FMusic')
    assert data.status_code == 404, 'Папка существует на диске или не удалось получить данные'
