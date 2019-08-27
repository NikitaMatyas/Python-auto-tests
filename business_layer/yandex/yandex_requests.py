import requests
import time
import allure


@allure.step
def get_disk_url():
    """ Получение URL адреса Яндекс Диска
    :return: URL адрес Яндекс Диска
    """
    return 'https://cloud-api.yandex.net/v1/disk/'


@allure.step
def get_token():
    """ Получения токена на авторизацию в API Яндекс Диска
    :return: Значение заголовка Authorization
    """
    token = 'AgAAAAAzRAFBAAXPTPomGUdTkEpIvhq_-sbAa_4'
    return 'OAuth ' + token


@allure.step
def get_disk_info(disk_url, token):
    """ Получение информации о Яндекс Диске
    :param disk_url: URL адрес Яндекс Диска
    :param token: Токен авторизации в API Яндекс Диска
    :return: Информацию о Яндекс Диске (результат запроса)
    """
    r = requests.get(disk_url, headers={'Authorization': token})
    return r


@allure.step
def create_folder(disk_url, token, path):
    """ Создание папки на Яндекс Диске
    :param disk_url: URL адрес Яндекс Диска
    :param token: Токен авторизации в API Яндекс Диска
    :param path: Путь к создаваемой папке (например %2FMusic)
    :return: Ссылка на мета-информацию о созданном ресурсе (результат запроса)
    """
    r = requests.put(disk_url + 'resources?path=' + path, headers={'Authorization': token})
    return r


@allure.step
def delete_resource(disk_url, token, path, del_property, wait_time):
    """ Удаление ресурса на Яндекс Диске
    :param disk_url: URL адрес Яндекс Диска
    :param token: Токен авторизации в API Яндекс Диска
    :param path: Путь к удаляемому ресурсу (например %2FMusic)
    :param del_property: Признак безвозвратного удаления, false - поместить в корзину, true - удалить безвозвратно
    :param wait_time: Количество секунд, которое нужно ждать между отправкой запросов на подтверждение
    :return: Код ответа без тела ответа (результат запроса)
    """
    r = requests.delete(disk_url + 'resources?path=' + path + '&permanently=' + del_property,
                        headers={'Authorization': token})
    if r.status_code == 202:
        return wait_for_success(r.json()["href"], token, wait_time)
    else:
        return r.status_code


@allure.step
def check_resource(disk_url, token, path):
    """ Проверка существования ресурса на Яндекс Диске
    :param disk_url: URL адрес Яндекс Диска
    :param token: Токен авторизации в API Яндекс Диска
    :param path: Путь к ресурсу (например %2FMusic)
    :return: Мета-информация о запрошенном ресурсе (результат запроса)
    """
    r = requests.get(disk_url + 'resources?path=' + path, headers={'Authorization': token})
    return r


@allure.step
def file_upload_link(disk_url, token, path):
    """ Получение URL адреса для загрузки файла в папку на Яндекс Диске
    :param disk_url: URL адрес Яндекс Диска
    :param token: Токен авторизации в API Яндекс Диска
    :param path: Путь по которому необходимо загрузить файл (например %2FMusic%2FSong.txt)
    :return: Результат запроса, Сгенерированный URL для загрузки файла
    """
    r = requests.get(disk_url + 'resources/upload?path=' + path, headers={'Authorization': token})
    return r, r.json()["href"]


@allure.step
def file_upload(path):
    """ Загрузка файла в папку на Яндекс Диске
    :param path: Сгенерированный URL для загрузки файла
    :return: Код ответа без тела ответа (результат запроса)
    """
    r = requests.put(path)
    return r


@allure.step
def restore_resource(disk_url, token, path, wait_time):
    """ Восстановление ресурса из корзины на Яндекс Диске
    :param disk_url: URL адрес Яндекс Диска
    :param token: Токен авторизации в API Яндекс Диска
    :param path: Путь по которому необходимо удалить ресурс (например %2FMusic%2FSong.txt)
    :param wait_time: Количество секунд, которое нужно ждать между отправкой запросов на подтверждение
    :return: Мета-информация о восстановленом ресурсе (результат запроса)
    """
    r = requests.put(disk_url + 'trash/resources/restore?path=' + path, headers={'Authorization': token})
    if r.status_code == 202:
        return wait_for_success(r.json()["href"], token, wait_time)
    else:
        return r.status_code


@allure.step
def wait_for_success(status_url, token, wait_time, interval=0.1):
    """ Ожидание подтверждения восстановления файла из корзины на Яндекс Диске
    :param status_url: URL адрес Яндекс Диска
    :param token: Токен авторизации в API Яндекс Диска
    :param wait_time: Время, в течении которого необходимо пытаться получить ответ
    :param interval: Частота, с которой запрос отправляется повторно
    :return: Код ответа без тела ответа (результат запроса)
    """
    start = time.time()
    r = requests.get(status_url, headers={'Authorization': token})
    if r.status_code == 200:
        if r.json()["status"] == 'failure':
            return 'Failure'
        elif r.json()["status"] == 'in-progress' and time.time() - start < wait_time:
            time.sleep(interval)
            wait_for_success(status_url, token, wait_time)
    return r.status_code


@allure.step
def clear_trash(disk_url, token, path, wait_time):
    """ Очистка корзины на Яндекс Диске
    :param disk_url: URL адрес Яндекс Диска
    :param token: Токен авторизации в API Яндекс Диска
    :param path: Путь по которому необходимо удалить ресурс (например %2FMusic)
    :param wait_time: Количество секунд, которое нужно ждать между отправкой запросов на подтверждение
    :return: Код ответа без тела ответа (результат запроса)
    """
    r = requests.delete(disk_url + 'trash/resources?path=' + path, headers={'Authorization': token})
    if r.status_code == 202:
        return wait_for_success(r.json()["href"], token, wait_time)
    else:
        return r.status_code
