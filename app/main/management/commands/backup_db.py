# D:\Python\myProject\bookshelves\app\main\management\commands\backup_db.py

'''
Для резервного копирования база данных в терминале
находясь в директории Джанго-проекта ввести команду:
python manage.py backup_db
'''

import os
from datetime import datetime
import shutil
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Create a backup copy of the database'

    def handle(self, *args, **options):
        # Директория для хранения резервных копий
        path_backup_folder = os.path.join('folder_files', 'backup_folder')

        if not os.path.exists(path_backup_folder):
            os.makedirs(path_backup_folder)  # Создаем директорию, если она не существует

        # Генерируем постфикс для имени резервной копии с использованием даты и времени
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Полное имя (в том числе относительный путь) файла резервной копии БД
        backup_file = os.path.join(path_backup_folder, f'db_backup_{timestamp}.sqlite3')

        # Get the path to db.sqlite3 from Django settings
        db_file_path = settings.DATABASES['default']['NAME']

        try:
            # Создать резервную копию
            shutil.copy(db_file_path, backup_file)
            self.stdout.write(self.style.SUCCESS(f'Created backup: {backup_file}'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error creating backup: {e}'))


