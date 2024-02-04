# D:\Python\myProject\bookshelves\app\audiobooks\models.py


from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from .utilities import translit_re, get_torrent_file_path, get_picture_file_path


class ModelCategories(models.Model):
    name = models.CharField(max_length=30, db_index=True, verbose_name="Категория")
    slug = models.SlugField(
        max_length=30, unique=True, db_index=True, verbose_name="URL"
    )

    def save(self, *args, **kwargs):
        # Генерируем уникальный слаг для категории
        self.slug = translit_re(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse("category", kwargs={"cat_slug": self.slug})

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["id"]


class ModelSubcategories(models.Model):
    category = models.ForeignKey(
        ModelCategories,
        on_delete=models.CASCADE,
        related_name="subcategories",
        verbose_name="Категория",
    )
    name = models.CharField(max_length=40, db_index=True, verbose_name="Жанр")
    slug = models.SlugField(
        max_length=60, unique=True, db_index=True, verbose_name="URL"
    )

    def save(self, *args, **kwargs):
        # Генерируем уникальный слаг для подкатегории
        self.slug = f"{translit_re(self.name)}"
        super().save(*args, **kwargs)

    def __str__(self):
        # return f"{self.category} - {self.name}"
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse(
            "subcategory",
            kwargs={"cat_slug": self.category.slug, "subcat_slug": self.slug},
        )

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"
        ordering = ["id"]


class Author(models.Model):
    name = models.CharField(max_length=60, unique=True, verbose_name="Имя")
    slug = models.SlugField(
        max_length=60, unique=True, db_index=True, verbose_name="URL"
    )

    def save(self, *args, **kwargs):
        # Генерируем уникальный слаг
        self.slug = translit_re(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse("author", kwargs={"author_slug": self.slug})

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"


class Reader(models.Model):
    name = models.CharField(max_length=60, unique=True, verbose_name="Имя")
    slug = models.SlugField(
        max_length=60, unique=True, db_index=True, verbose_name="URL"
    )

    def save(self, *args, **kwargs):
        # Генерируем уникальный слаг
        self.slug = translit_re(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse("average_rating", kwargs={"reader_slug": self.slug})

    class Meta:
        verbose_name = "Чтец"
        verbose_name_plural = "Чтецы"


class Cycle(models.Model):
    name = models.CharField(max_length=60, unique=True, verbose_name="Имя")
    slug = models.SlugField(
        max_length=60, unique=True, db_index=True, verbose_name="URL"
    )
    description = models.TextField(blank=True, null=True, verbose_name="Описание цикла")

    def save(self, *args, **kwargs):
        # Генерируем уникальный слаг
        self.slug = translit_re(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse("cycle", kwargs={"cycle_slug": self.name})

    class Meta:
        verbose_name = "Цикл"
        verbose_name_plural = "Циклы"


class ModelBooks(models.Model):
    id_old = models.IntegerField(
        unique=True, null=True, blank=True, verbose_name="id_old"
    )
    title = models.CharField(max_length=60, verbose_name="Заголовок")
    slug = models.SlugField(
        max_length=120, unique=True, db_index=True, verbose_name="URL"
    )
    book_subcategories = models.ManyToManyField(
        "ModelSubcategories", blank=False, default=None, verbose_name="Жанры"
    )
    cycle = models.ForeignKey(
        Cycle, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Цикл"
    )
    number_in_cycle = models.IntegerField(
        null=True, blank=True, verbose_name="Номер в цикле"
    )
    authors = models.ManyToManyField(Author, blank=True, verbose_name="Авторы")
    readers = models.ManyToManyField(Reader, blank=True, verbose_name="Чтецы")
    year = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Год",
    )
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    duration = models.CharField(max_length=60, verbose_name="Продолжительность")
    quality = models.CharField(max_length=60, verbose_name="Качество")

    size = models.CharField(
        null=True, blank=True, max_length=30, verbose_name="Размер"
    )
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    subdirectory = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        default='999',
        verbose_name="Поддиректория файлов",
    )
    torrent = models.FileField(
        upload_to=get_torrent_file_path,
        blank=True,
        null=True,
        verbose_name="Торрент-файл"
    )
    picture = models.ImageField(
        upload_to=get_picture_file_path,
        blank=True,
        null=True,
        verbose_name="Картинка"
    )
    like = models.IntegerField(default=0, verbose_name="Нравится(+)")
    dislike = models.IntegerField(default=0, verbose_name="Не нравится(-)")
    total_comments = models.IntegerField(default=0, verbose_name="Всего комментариев")
    is_published = models.BooleanField(default=True, verbose_name="Публикация")

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse("book", kwargs={"book_slug": self.slug})

    class Meta:
        verbose_name = "Аудиокнига"
        verbose_name_plural = "Аудиокниги"  # уточнить названия
        ordering = ["-year", "title"]  # сортировка по дате убывания


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
