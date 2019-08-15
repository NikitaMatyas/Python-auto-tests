from business_layer.yandex.yandex_requests import *
from framework_core.variables import disk_url, token


def test_tc_004():
    """ Получение информацию о диске пользователя, создание папки/файлов и сравнение размеров
    1. Получение информации о диске пользователя (Код ответа == 200, размер корзины)
    2. Создание папки на Яндекс Диске (Код ответа == 201)
    3. Генерация 3 ссылок для загрузки файла на Яндекс Диск (Код ответа == 200)
    4. Загрузка 3 файлов по сгенерированному URL (Код ответа == 201)
    5. Помещение 3 файлов в корзину (Код ответа == 204 или 200)
    6. Получение размера файлов в корзине (Код ответа == 200, суммарный размер трех файлов в корзине)
    7. Получение информации о диске пользователя (Код ответа == 200, размер корзины)
    8. Сравнение финального размера корзины с начальным + размером файлов (Размер совпадает, код ответа == 200)
    9. Восстановление 3 файлов из корзины (Код ответа == 200)
    10. Удаление папки с файлами на Яндекс Диске (Код ответа == 204 или 200)
    """
    data = get_disk_info(disk_url, token)
    assert data.status_code == 200, 'Не удалось получить информацию о диске пользователя'
    initial_trash_size = int(data.json()["trash_size"])

    data = create_folder(disk_url, token, '%2FMusic')
    assert data.status_code == 201, 'Не удалось создать папку на Яндекс диске'

    paths_1 = ['%2FMusic%2FSong_1.txt', '%2FMusic%2FSong_2.txt', '%2FMusic%2FSong_3.txt']
    for i in paths_1:
        data, url = file_upload_link(disk_url, token, i)
        assert data.status_code == 200, 'Не удалось получить URL для загрузки файла на Яндекс диск'

        data = file_upload(url)
        assert data.status_code == 201, 'Не удалось загрузить файл по сгенерированному URL'

    for i in paths_1:
        data = delete_resource(disk_url, token, i, "false", 1)
        assert data == 204 or data == 200, 'Не удалось поместить ресурс в корзину'

    paths_2 = ['%2FSong_1.txt', '%2FSong_2.txt', '%2FSong_3.txt']
    files_size = 0
    for i in paths_2:
        data = check_resource(disk_url + 'trash/', token, i)
        assert data.status_code == 200, 'Не удалось получить информацию о ресурсе'
        files_size += int(data.json()["size"])

    data = get_disk_info(disk_url, token)
    assert data.status_code == 200, 'Не удалось получить информацию о диске пользователя'
    final_trash_size = int(data.json()["trash_size"])
    assert final_trash_size == initial_trash_size + files_size, \
        'Размер файлов в корзине не совпадает с начальным размером корзины + размером файлов'

    for i in paths_2:
        data = restore_resource(disk_url, token, i, 1)
        assert data == 201 or data == 200, 'Не удалось восстановить ресурс на Яндекс диске'

    data = delete_resource(disk_url, token, "%2FMusic", "true", 1)
    assert data == 204 or data == 200, 'Не удалось удалить папку на Яндекс диске'
