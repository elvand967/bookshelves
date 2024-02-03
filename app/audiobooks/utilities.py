# D:\Python\myProject\bookshelves\app\audiobooks\utilities.py
import os
import re

from django.conf import settings


def get_torrent_file_path(instance, filename):
    # Получаем значения из экземпляра модели
    subdirectory = instance.subdirectory

    # Генерируем относительный путь
    relative_path = os.path.join('files_torrent', subdirectory, filename)

    return relative_path


def get_picture_file_path(instance, filename):
    # Получаем значения из экземпляра модели
    subdirectory = instance.subdirectory

    # Генерируем относительный путь
    relative_path = os.path.join('files_picture', subdirectory, filename)

    return relative_path


def translit_re(input_str):
    ''' Обеспечение транслитерации кириллицы (и другие символы - непотребности) в латиницу,
    re (регулярные выражения):
    Преимущества:
    Гибкость и контроль над процессом транслитерации с использованием регулярных выражений.
    Полный контроль над символами, которые подлежат замене.
    Недостатки:
    Требует более длинного кода, особенно если нужно обработать много разных символов.
    '''
    translit_dict = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e', 'ж': 'zh', 'з': 'z', 'и': 'i',
        'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
        'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ъ': '', 'ы': 'y', 'ь': '',
        'э': 'e', 'ю': 'yu', 'я': 'ya', 'ґ': 'g', 'є': 'ie', 'ї': 'i', 'і': 'i',
        'ç': 'c', 'ş': 's', 'ğ': 'g', 'ı': 'i',
        'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'ß': 'ss',
        'à': 'a', 'è': 'e', 'é': 'e', 'ê': 'e', 'ô': 'o', 'û': 'u', 'â': 'a',
        'а̑': 'a', 'э̑': 'e', 'и̑': 'i', 'о̑': 'o', 'у̑': 'u', 'ĭ': 'y',
        '0': '0', '1': '1', '2': '2', '3': '3', '4': '4',
        '5': '5', '6': '6', '7': '7', '8': '8', '9': '9',
    }

    # Добавим символы, подлежащие замене
    translit_dict.update({
        '?': '_', '<': '_', '>': '_', ' ': '_', '~': '_', '@': '_', '"': '_', "'": '_', ':': '_',
        ';': '_', '#': '_', '$': '_', '&': '_', '*': '_', '(': '_', ')': '_', '\\': '_', '|': '_',
        '/': '_', '.': '_',
        '«': '_', '»': '_',
        ',': '_', '!': '_',
        '‐': '-', '−': '-', '–': '-', '—': '-', '-': '-',
        '“': '_', '”': '_',
    })

    # Заменяем все символы, кроме латинских букв и "-"
    output_str = ''.join([translit_dict.get(char.lower(), char) for char in input_str])

    # Заменяем множественные подчеркивания на одно
    output_str = re.sub('_+', '_', output_str)

    # Удаление подчеркиваний в начале и конце строки
    output_str = output_str.strip('_')

    # Заменяем множественные дефисы на одно
    output_str = re.sub('-+', '-', output_str)

    # Удаление дефисов в начале и конце строки
    output_str = output_str.strip('-')

    return output_str.lower()

# print(f'Вызов функции translit_re("圣骑士的传说"): {translit_re("圣骑士的传说")}')
