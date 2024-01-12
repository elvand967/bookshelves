# D:\Python\myProject\bookshelves\app\main\management\commands\add_ratings.py
'''
Для искусственного обновления данных AverageRating
находясь в директории Джанго-проекта ввести команду:

python manage.py add_ratings

'''

import random

from django.core.management.base import BaseCommand
from rating.models import AverageRating

class Command(BaseCommand):
    help = 'Дополнительное обновления данных AverageRating'

    def handle(self, *args, **options):
        add_number_votes = 10

        for rating in AverageRating.objects.all():
            add_sum_plot = random.randrange(67, 77)  # сюжет
            add_sum_writing_talent = random.randrange(69, 79)  # Писательский талант
            add_sum_voice_quality = random.randrange(65, 75)  # Качество озвучивания

            rating.number_votes = rating.number_votes + add_number_votes
            rating.sum_points_plot = rating.sum_points_plot + add_sum_plot
            rating.sum_points_writing_talent = rating.sum_points_writing_talent + add_sum_writing_talent
            rating.sum_points_voice_quality = rating.sum_points_voice_quality + add_sum_voice_quality

            # # почистим концы, значение сум рейтингов доведем до 1-го знака после запятой
            # rating.sum_points_plot = round(rating.sum_points_plot, 1)
            # rating.sum_points_writing_talent = round(rating.sum_points_writing_talent, 1)
            # rating.sum_points_voice_quality = round(rating.sum_points_voice_quality, 1)

            rating.save()

        self.stdout.write(self.style.SUCCESS('Успешно дополнены данные AverageRating.'))
