import requests
import time


def get_disk_url():
    """ Получение URL адреса Яндекс Диска
    :return: URL адрес Яндекс Диска
    """
    return 'https://cloud-api.yandex.net/v1/disk/'


def get_token():
    """ Получения токена на авторизацию в API Яндекс Диска
    :return: Значение заголовка Authorization
    """
    token = 'AgAAAAAzRAFBAAXPTPomGUdTkEpIvhq_-sbAa_4'
    return 'OAuth ' + token


def get_disk_info(disk_url, token):
    """ Получение информации о Яндекс Диске
    :param disk_url: URL адрес Яндекс Диска
    :param token: Токен авторизации в API Яндекс Диска
    :return: Информацию о Яндекс Диске (результат запроса)
    """
    r = requests.get(disk_url, headers={'Authorization': token})
    return r


def create_folder(disk_url, token, path):
    """ Создание папки на Яндекс Диске
    :param disk_url: URL адрес Яндекс Диска
    :param token: Токен авторизации в API Яндекс Диска
    :param path: Путь к создаваемой папке (например %2FMusic)
    :return: Ссылка на мета-информацию о созданном ресурсе (результат запроса)
    """
    r = requests.put(disk_url + 'resources?path=' + path, headers={'Authorization': token})
    return r


def delete_folder(disk_url, token, path, del_property):
    """ Удаление папки на Яндекс Диске
    :param disk_url: URL адрес Яндекс Диска
    :param token: Токен авторизации в API Яндекс Диска
    :param path: Путь к удаляемой папке (например %2FMusic)
    :param del_property: Признак безвозвратного удаления, false - поместить в корзину, true - удалить безвозвратно
    :return: Код ответа без тела ответа (результат запроса)
    """
    r = requests.delete(disk_url + 'resources?path=' + path + '&permanently=' + del_property,
                        headers={'Authorization': token})
    return r


def check_folder(disk_url, token, path):
    """ Проверка существования папки на Яндекс Диске
    :param disk_url: URL адрес Яндекс Диска
    :param token: Токен авторизации в API Яндекс Диска
    :param path: Путь к удаляемой папке (например %2FMusic)
    :return: Мета-информация о запрошенном ресурсе (результат запроса)
    """
    r = requests.get(disk_url + 'resources?path=' + path, headers={'Authorization': token})
    return r


def file_upload_link(disk_url, token, path):
    """ Получение URL адреса для загрузки файла в папку на Яндекс Диске
    :param disk_url: URL адрес Яндекс Диска
    :param token: Токен авторизации в API Яндекс Диска
    :param path: Путь по которому необходимо загрузить файл (например %2FMusic%2FSong.txt)
    :return: Результат запроса, Сгенерированный URL для загрузки файла
    """
    r = requests.get(disk_url + 'resources/upload?path=' + path, headers={'Authorization': token})
    return r, r.json()["href"]


def file_upload(path):
    """ Загрузка файла в папку на Яндекс Диске
    :param path: Сгенерированный URL для загрузки файла
    :return: Код ответа без тела ответа (результат запроса)
    """
    r = requests.put(path)
    return r


def delete_file(disk_url, token, path, del_property):
    """ Удаление файла из папки на Яндекс Диске
    :param disk_url: URL адрес Яндекс Диска
    :param token: Токен авторизации в API Яндекс Диска
    :param path: Путь по которому необходимо удалить файл (например %2FMusic%2FSong.txt)
    :param del_property: Признак безвозвратного удаления, false - поместить в корзину, true - удалить безвозвратно
    :return: Код ответа без тела ответа (результат запроса)
    """
    r = requests.delete(disk_url + 'resources?path=' + path + '&permanently=' + del_property,
                        headers={'Authorization': token})
    return r


def restore_file(disk_url, token, path):
    """ Восстановление файла из корзины на Яндекс Диске
    :param disk_url: URL адрес Яндекс Диска
    :param token: Токен авторизации в API Яндекс Диска
    :param path: Путь по которому необходимо удалить файл (например %2FMusic%2FSong.txt)
    :return: Мета-информация о восстановленом ресурсе (результат запроса)
    """
    r = requests.put(disk_url + 'trash/resources/restore?path=' + path, headers={'Authorization': token})
    return r


def wait_for_restore(status_url, token, wait_time):
    """ Ожидание подтверждения восстановления файла из корзины на Яндекс Диске
    :param status_url: URL адрес Яндекс Диска
    :param token: Токен авторизации в API Яндекс Диска
    :param wait_time: Количество секунд, которое нужно ждать между отправкой запросов на подтверждение
    :return:
    """
    condition = False
    while not condition:
        r = requests.get(status_url, headers={'Authorization': token})
        if r.json()["status"] == 'success':
            condition = True
        time.sleep(wait_time)
