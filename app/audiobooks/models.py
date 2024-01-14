# D:\Python\myProject\bookshelves\app\audiobooks\models.py


import os
from django.conf.global_settings import MEDIA_ROOT
from django.db import models
from django.urls import reverse

from .utilities import translit_re, get_torrent_file_path, get_picture_file_path
# from ..app import settings


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
