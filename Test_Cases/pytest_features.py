import pytest
import sys

'''
# Базовые фикстуры, setup - вызывается перед тестом, teardown - после теста
def setup():
    print("basic setup into module")


def teardown():
    print("basic teardown into module")
'''

# Расширенные фикстуры
''' Для создания расширенной фикстуры в PyTest необходимо:
1) Импортировать модуль pytest
2) Использовать декоратор @pytest.fixture(), чтобы обозначить, что данная функция является фикстурой
3) Задать уровень фикстуры (scope). Возможные значения "function", "cls", "module", "session". Значение по умолчанию =
"function"
4) Если необходим вызов teardown для этой фикстуры, то надо добавить в него финализатор (через метод addfinalizer 
объекта request передаваемого в фикстуру)
5) Добавить имя данной фикстуры в список параметров функции
'''


@pytest.fixture()
def resource_setup(request):
    print("resource setup")

    def resource_teardown():
        print("resource_teardown")
    request.addfinalizer(resource_teardown)


def test_1_that_needs_resource(resource_setup):
    print("test_1_that_needs_resource")


def test_2_that_does_not():
    print("test_2_that_does_not")


def test_3_that_does_again(resource_setup):
    print("test_3_that_does_again")


# Другой способ вызова расширенных фикстур - декорирование теста декоратором @pytest.mark.usefixtures()
@pytest.mark.usefixtures("resource_setup")
def test_3_that_does_again():
    print("test_3_that_does_again")


# Более простой способ осуществить teardown расширенной фикстуры - использование конструкции yield
@pytest.yield_fixture()
def resource_setup():
    print("resource_setup")
    yield
    print("resource_teardown")


@pytest.mark.usefixtures("resource_setup")
def test_3_that_does_again():
    print("test_3_that_does_again")


# Фикстура может возвращать значение
@pytest.fixture(scope="module")
def resource_setup(request):
    print("\nconnect to db")
    db = {"Red": 1, "Blue": 2, "Green": 3}

    def resource_teardown():
        print("\ndisconnect")

    request.addfinalizer(resource_teardown)
    return db


def test_db(resource_setup):
    for k in resource_setup.keys():
        print("color {0} has id {1}".format(k, resource_setup[k]))


''' Уровень фикстуры (scope):
1) function - фикстура запускается для каждого теста
2) cls - фикстура запускается для каждого класса
3) module - фикстура запускается для каждого модуля
4) session - фикстура запускается для каждой сессии (то есть фактически один раз)

Также фикстуры можно описывать в файле conftest.py, который автоматически импортируется PyTest. При этом фикстура может 
иметь любой уровень (только через описание в этом файле можно создать фикстуру с уровнем «сессия»).
'''


# Параметризация (запуск одного и того же теста с разным набором входных параметров)
@pytest.mark.parametrize("x", [1, 2])
def test_params(x):
    print("x: {0}".format(x))
    assert True

# Если указать несколько меток с разными параметрами, то тест будет запущен со всеми возможными наборами параметров
@pytest.mark.parametrize("x", [1, 2])
@pytest.mark.parametrize("y", [10, 11])
def test_params_cross(x, y):
    print("x: {0}, y: {1}".format(x, y))
    assert True


# Метки
''' PyTest поддерживает класс декораторов @pytest.mark называемый «метками». Базовый список включает в себя следующие:
1) @pytest.mark.parametrize — для параметризации тестов
2) @pytest.mark.xfail – помечает, что тест должен не проходить и PyTest будет воспринимать это, как ожидаемое поведение 
(полезно, как временная метка для тестов на разрабатываемые функции). 
3) @pytest.mark.skipif – позволяет задать условие при выполнении которого тест будет пропущен
4) @pytest.mark.usefixtures – позволяет перечислить все фикстуры, вызываемые для теста
'''


@pytest.mark.xfail()
def test_failed():
    assert False


@pytest.mark.xfail(sys.platform != "win64", reason="requires windows 64bit")
def test_failed_for_not_win32_systems():
    assert False


@pytest.mark.skipif(sys.platform != "win64", reason="requires windows 64bit")
def test_skipped_for_not_win64_systems():
    assert False


''' Метки могут быть произвольно заданы пользователем. Что позволяет выделять наборы тестов для отдельного запуска по 
имени метки, передавая ее с ключем -m
Метку можно описать и сделать доступной для всех модулей, через описание ее в модуле pytest.ini. 
При этом она появится в списке доступных меток, получаемых через «py.test --markers».

Например, содержимое pytest.ini:
[pytest]
markers =
    critical_test: mark test as critical. These tests must to be checked first.
'''


def test_1():
    print("test_1")


#@pytest.mark.critital_tests
def test_2():
    print("test_2")


def test_3():
    print("test_3")

# Запускаем как pytest -s pytest_features.py -s -m "critical_tests"


''' Обработка исключений
Pytest также позволяет проверять корректность возвращаемых исключений при помощи with pytest.raises()
'''


def test_exception():
    with pytest.raises(ZeroDivisionError):
        print(1 / 0)
