# D:\Python\myProject\bookshelves\app\rating\models.py

from django.db import models
from django.urls import reverse

from audiobooks.models import ModelBooks
from django.contrib.auth.models import User

class UserRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(ModelBooks, on_delete=models.CASCADE, related_name='user_ratings')
    plot = models.IntegerField(default=0, verbose_name="Сюжет")
    talent = models.IntegerField(default=0, verbose_name="Писательский талант")
    voice = models.IntegerField(default=0, verbose_name="Качество озвучивания")
    like_dislike = models.IntegerField(verbose_name="Лайк/Дизлайк", null=True, blank=True)

    def save(self, *args, **kwargs):
        # 1. Получаем связанный объект `rating`
        rating = self.book.rating

        # Предшествующие оценки пользователя
        old_ratings = {
            'plot': self.plot if hasattr(self, 'plot') else None,
            'talent': self.talent if hasattr(self, 'talent') else None,
            'voice': self.voice if hasattr(self, 'voice_quality') else None,
        }

        # Новые оценки пользователя
        new_ratings = {
            'plot': getattr(self, 'plot', None),
            'talent': getattr(self, 'talent', None),
            'voice': getattr(self, 'voice', None),
        }

        # Количество голосов
        votes = 1  # Предположим, что это новый голос пользователя
        if not self._state.adding:
            # Если это не новая запись, то это редактирование или удаление
            votes = 0 if kwargs.get('update_fields') else -1

        for rating_type in old_ratings.keys():
            rating.update_rating(
                rating_type,
                old_ratings[rating_type],
                new_ratings[rating_type],
                votes
            )

        # Обновляем лайки и дизлайки
        rating.update_likes_dislikes(self.like_dislike, self.like_dislike)

        # Сохраняем оценку пользователя
        super().save(*args, **kwargs)


class AverageRating(models.Model):
    book = models.OneToOneField(ModelBooks, on_delete=models.CASCADE, related_name='average_rating', verbose_name="Книга")
    downloads = models.IntegerField(default=0, null=True, blank=True, verbose_name="Количество загрузок")
    number_votes = models.IntegerField(default=0, null=True, blank=True, verbose_name="Количество голосов")

    sum_plot = models.IntegerField(default=0, verbose_name="Сюжет, все балы")
    plot = models.FloatField(default=0.0, verbose_name="Сюжет, средний бал")

    sum_talent = models.IntegerField(default=0, verbose_name="Писательский талант, все балы")
    talent = models.FloatField(default=0.0, verbose_name="Писательский талант, средний бал")

    sum_voice = models.IntegerField(default=0, verbose_name="Качество озвучивания, все балы")
    voice = models.FloatField(default=0.0, verbose_name="Качество озвучивания, средний бал")

    total_ratings = models.FloatField(default=0, verbose_name="Общий рейтинг")
    like = models.IntegerField(default=0, verbose_name="Нравится(+)")
    dislike = models.IntegerField(default=0, verbose_name="Не нравится(-)")

    def __str__(self):
        return f"Рейтинг для книги {self.book.title}"

    def get_absolute_url(self):
        return reverse('имя вашего URL-шаблона', args=[str(self.book.id)])

    def update_rating(self, rating_type, user_rating_old, user_rating_new, votes):
        current_rating = getattr(self, rating_type)
        if votes > 0:
            # Пользователь впервые голосует
            setattr(self, rating_type, current_rating + user_rating_new)
        elif votes == 0:
            # Пользователь решил изменить свою оценку
            setattr(self, rating_type, current_rating - user_rating_old + user_rating_new)
        elif votes < 0:
            # Пользователь удален, отнимаем его оценку
            setattr(self, rating_type, current_rating - user_rating_old)

        self.number_votes += votes

        self.save()

    def update_likes_dislikes(self, old, new):
        if old is None and new is not None:
            # Пользователь впервые поставил лайк/дизлайк
            if new:
                self.like += 1
            else:
                self.dislike += 1
        elif old is not None and new is not None:
            # Пользователь изменил свой лайк/дизлайк
            if old:
                self.like -= 1
            else:
                self.dislike -= 1
            if new:
                self.like += 1
            else:
                self.dislike += 1
        elif old is not None and new is None:
            # Пользователь удалил свой лайк/дизлайк
            if old:
                self.like -= 1
            else:
                self.dislike -= 1
        self.save()

    def save(self, *args, **kwargs):
        # Пересчет среднего бала по формуле
        self.plot = round(self.sum_plot / self.number_votes, 1) if self.number_votes > 0 else 0.0
        self.talent = round(self.sum_talent / self.number_votes, 1) if self.number_votes > 0 else 0.0
        self.voice = round(self.sum_voice / self.number_votes, 1) if self.number_votes > 0 else 0.0

        # Пересчет общего рейтинга
        self.total_ratings = round((self.plot + self.talent + self.voice) / 3, 1)

        super().save(*args, **kwargs)
