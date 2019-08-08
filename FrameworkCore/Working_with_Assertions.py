print('Assertions \n')

'''
- сравнение двух чисел
- сравнение двух строк на полное совпадение
- сравнение двух строк на частичное совпадени(содержит)
- сравнение массивов
- изучение всех ассершинов инструмента
'''


def num_comp(a, b):
    assert a == b, 'Numbers are not equal'


def str_comp(str1, str2):
    assert str1 == str2, 'Strings are not equal'


def str_part_comp(str1, str2):
    assert str2 in str1, 'No string #2 in string #1'


def arrays_comp(array1, array2):
    assert array1 == array2, 'Arrays are not equal'


num_comp(5, 2)
str_comp('hello', 'world')
str_part_comp('ABChelloABC', 'hello')

arr1 = [1, 2, 3, 4, 5, 6]
arr2 = [1, 2, 3, 4, 5, 6]
arrays_comp(arr1, arr2)
