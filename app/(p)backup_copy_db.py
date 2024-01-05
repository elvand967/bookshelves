# D:\Python\myProject\bookshelves\app\(p)backup_copy_db.py

import os
from datetime import datetime
import shutil

def main():
    print(f"{' Резервное копирование базы данных ':.^50}")
    print(f"{' Режим: работа с кодом Python ':-^50}\n")
    stop = input('Для продолжения нажмите любую клавишу,\nдля остановки нажмите "Q" ')
    if stop.upper() == "Q" or stop.upper() == "Й":
        return
    # Резервная копия Базы данных
    database_backup()


def database_backup():
    # Директория для хранения резервных копий
    # path_backup_folder = os.path.join('..', '..', '..', 'folder_files', 'backup_folder')
    path_backup_folder = os.path.join('folder_files', 'backup_folder')

    if not os.path.exists(path_backup_folder):
        os.makedirs(path_backup_folder)  # Создаем директорию, если она не существует

    # Генерируем постфикс для имени резервной копии с использованием даты и времени
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Полное имя (в том числе относительный путь) файла резервной копии БД
    backup_file = os.path.join(path_backup_folder, f'db_backup_{timestamp}.sqlite3')

    try:
        # Создать резервную копию
        # shutil.copy(os.path.join('..', '..', '..', 'db.sqlite3'), backup_file)
        shutil.copy(os.path.join('db.sqlite3'), backup_file)
        print(f'Создана резервная копия: {backup_file}')
    except Exception as e:
        print(f'Ошибка при создании резервной копии: {e}')


if __name__ == "__main__":
    main()