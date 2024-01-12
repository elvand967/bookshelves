# D:\Python\myProject\bookshelves\app\rating\models.py


from django.db import models
from django.contrib.auth.models import User
from audiobooks.models import ModelBooks
import random


class AverageRating(models.Model):
    book = models.OneToOneField(ModelBooks, on_delete=models.CASCADE, related_name='average_rating',
                                verbose_name="Книга")
    number_votes = models.IntegerField(default=1, null=True, blank=True, verbose_name="Количество голосов")

    sum_points_plot = models.FloatField(default=random.uniform(6.9, 9.0), verbose_name="Сюжет, все балы")
    plot = models.FloatField(default=0.0, verbose_name="Сюжет, средний бал")

    sum_points_writing_talent = models.FloatField(default=random.uniform(6.7, 9.0),
                                                  verbose_name="Писательский талант, все балы")
    writing_talent = models.FloatField(default=0.0, verbose_name="Писательский талант, средний бал")

    sum_points_voice_quality = models.FloatField(default=random.uniform(7.5, 9.0),
                                                 verbose_name="Качество озвучивания, все балы")
    voice_quality = models.FloatField(default=0.0, verbose_name="Качество озвучивания, средний бал")

    total_ratings = models.IntegerField(default=0, verbose_name="Общий рейтинг")
    like = models.IntegerField(default=random.randrange(3, 8), verbose_name="Нравится(+)")
    dislike = models.IntegerField(default=random.randrange(1, 4), verbose_name="Не нравится(-)")

    def save(self, *args, **kwargs):
        # Пересчет среднего бала по формуле
        self.plot = round(self.sum_points_plot / self.number_votes, 1) if self.number_votes > 0 else 0.0
        self.writing_talent = round(self.sum_points_writing_talent / self.number_votes,
                                    1) if self.number_votes > 0 else 0.0
        self.voice_quality = round(self.sum_points_voice_quality / self.number_votes,
                                   1) if self.number_votes > 0 else 0.0

        # Пересчет общего рейтинга
        self.total_ratings = round((self.plot + self.writing_talent + self.voice_quality) / 3)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.book.title} - Average Ratings"


