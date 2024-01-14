# D:\Python\myProject\bookshelves\app\main\management\commands\InitializeRatings.py
'''
Для начальной инициализации данных AverageRating
(при загруженных экземпляров модели `ModelBooks`),
находясь в директории Джанго-проекта ввести команду:

python manage.py InitializeRatings
'''
from django.core.management.base import BaseCommand
from django.db.models import Q
import random

from audiobooks.models import ModelBooks
from rating.models import AverageRating

class Command(BaseCommand):
    help = 'Инициализируйте данные AverageRating из существующих данных ModelBooks.' \
           'Initialize AverageRating data from existing ModelBooks data'

    def handle(self, *args, **options):
        print(f"{' Инициализация данных AverageRating ':-^50}\n")
        stop = input('Для продолжения нажмите любую клавишу,\nдля остановки нажмите "Q" ')
        if stop.upper() == "Q" or stop.upper() == "Й":
            exit()
        start_id = int(input("начальный id ModelBooks: "))
        end_id = int(input("конечный id ModelBooks: "))
        if start_id > end_id:
            end_id = start_id

        number_votes = 10

        for book in ModelBooks.objects.filter(Q(pk__gte=start_id) & Q(pk__lte=end_id)):
            # Проверка существования записи с book_id = book.id
            if AverageRating.objects.filter(book_id=book.id).exists():
                self.stdout.write(self.style.SUCCESS(f'Для книги "{book.title}" уже существует экземпляр AverageRating. Пропускаем.'))
                continue

            # Создание экземпляра AverageRating для каждой существующей книги
            AverageRating.objects.create(
                book=book,
                downloads=random.randrange(20, 50),
                number_votes=number_votes-1,
                sum_plot=random.randrange(3, 9) * number_votes,
                sum_talent=random.randrange(3, 9) * number_votes,
                sum_voice=random.randrange(3, 9) * number_votes,
                like=random.randrange(5, 20),
                dislike=random.randrange(3, 7),
                # Добавьте другие поля, которые вы хотите скопировать с ModelBooks
            )

        self.stdout.write(self.style.SUCCESS('Успешно инициализированы данные AverageRating.'))
