# D:\Python\myProject\bookshelves\app\main\management\commands\initialize_ratings.py
'''
Для начальной инициализации данных AverageRating
(при загруженной модели `ModelBooks`),
находясь в директории Джанго-проекта ввести команду:

python manage.py initialize_ratings
'''

from django.core.management.base import BaseCommand

from audiobooks.models import ModelBooks
from rating.models import AverageRating

class Command(BaseCommand):
    help = 'Инициализируйте данные AverageRating из существующих данных ModelBooks.' \
           'Initialize AverageRating data from existing ModelBooks data'

    def handle(self, *args, **options):
        for book in ModelBooks.objects.all():
            # Создаем экземпляр AverageRating для каждой существующей книги
            AverageRating.objects.create(
                book=book,
                # Добавьте другие поля, которые вы хотите скопировать с ModelBooks
            )

        self.stdout.write(self.style.SUCCESS('Успешно инициализированы данные AverageRating.'))
