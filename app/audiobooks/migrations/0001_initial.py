# Generated by Django 4.2.8 on 2024-01-04 08:15

import audiobooks.utilities
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60, unique=True, verbose_name='Имя')),
                ('slug', models.SlugField(max_length=60, unique=True, verbose_name='URL')),
            ],
            options={
                'verbose_name': 'Автор',
                'verbose_name_plural': 'Авторы',
            },
        ),
        migrations.CreateModel(
            name='Cycle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60, unique=True, verbose_name='Имя')),
                ('slug', models.SlugField(max_length=60, unique=True, verbose_name='URL')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание цикла')),
            ],
            options={
                'verbose_name': 'Цикл',
                'verbose_name_plural': 'Циклы',
            },
        ),
        migrations.CreateModel(
            name='ModelCategories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=30, verbose_name='Категория')),
                ('slug', models.SlugField(max_length=30, unique=True, verbose_name='URL')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Reader',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60, unique=True, verbose_name='Имя')),
                ('slug', models.SlugField(max_length=60, unique=True, verbose_name='URL')),
            ],
            options={
                'verbose_name': 'Чтец',
                'verbose_name_plural': 'Чтецы',
            },
        ),
        migrations.CreateModel(
            name='ModelSubcategories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=40, verbose_name='Жанр')),
                ('slug', models.SlugField(max_length=60, unique=True, verbose_name='URL')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='audiobooks.modelcategories', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Жанр',
                'verbose_name_plural': 'Жанры',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='ModelBooks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_old', models.IntegerField(blank=True, null=True, unique=True, verbose_name='id_old')),
                ('title', models.CharField(max_length=60, verbose_name='Заголовок')),
                ('slug', models.SlugField(max_length=120, unique=True, verbose_name='URL')),
                ('year', models.IntegerField(blank=True, null=True, verbose_name='Год')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('time_update', models.DateTimeField(auto_now=True, verbose_name='Время изменения')),
                ('duration', models.CharField(max_length=60, verbose_name='Продолжительность')),
                ('quality', models.CharField(max_length=60, verbose_name='Качество')),
                ('number_in_cycle', models.IntegerField(blank=True, null=True, verbose_name='Номер в цикле')),
                ('size', models.CharField(blank=True, max_length=30, null=True, verbose_name='Размер')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('subdirectory', models.CharField(blank=True, default='999', max_length=10, null=True, verbose_name='Поддиректория файлов')),
                ('torrent', models.FileField(blank=True, null=True, upload_to=audiobooks.utilities.get_torrent_file_path, verbose_name='Торрент-файл')),
                ('picture', models.ImageField(blank=True, null=True, upload_to=audiobooks.utilities.get_picture_file_path, verbose_name='Картинка')),
                ('like', models.IntegerField(default=0, verbose_name='Нравится(+)')),
                ('dislike', models.IntegerField(default=0, verbose_name='Не нравится(-)')),
                ('total_comments', models.IntegerField(default=0, verbose_name='Всего комментариев')),
                ('is_published', models.BooleanField(default=True, verbose_name='Публикация')),
                ('authors', models.ManyToManyField(blank=True, to='audiobooks.author', verbose_name='Авторы')),
                ('book_subcategories', models.ManyToManyField(default=None, to='audiobooks.modelsubcategories', verbose_name='Жанры')),
                ('cycle', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='audiobooks.cycle', verbose_name='Цикл')),
                ('readers', models.ManyToManyField(blank=True, to='audiobooks.reader', verbose_name='Чтецы')),
            ],
            options={
                'verbose_name': 'Аудиокнига',
                'verbose_name_plural': 'Аудиокниги',
                'ordering': ['-year', 'title'],
            },
        ),
    ]
