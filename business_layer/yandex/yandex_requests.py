import requests


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


def delete_folder(disk_url, token, path):
    """ Удаление папки на Яндекс Диске
    :param disk_url: URL адрес Яндекс Диска
    :param token: Токен авторизации в API Яндекс Диска
    :param path: Путь к удаляемой папке (например %2FMusic)
    :return: Код ответа без тела ответа (результат запроса)
    """
    r = requests.delete(disk_url + 'resources?path=' + path, headers={'Authorization': token})
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
