# D:\Python\myProject\bookshelves\app\(p)downloading_new_books.py

# Служебные утилиты
import os
from django import setup

from audiobooks.utilities import translit_re


# Устанавливаем переменную окружения, указывающую Django, в каком проекте искать настройки
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
# Настраиваем Django
setup()
import sys
sys.path.append("/")


import re
from django.db import connections, IntegrityError
from audiobooks.models import ModelBooks, Author, Reader, Cycle, ModelSubcategories, ModelCategories
from django.core.exceptions import ObjectDoesNotExist

def main():
    print(f"{' Загрузка из `database_books.db` ':-^50}")
    print(f"{' Режим: работа с кодом Python ':+^50}\n")
    stop = input('Для продолжения нажмите любую клавишу,\nдля остановки нажмите "Q" ')
    if stop.upper() == "Q" or stop.upper() == "Й":
        return
    start_id = int(input("начальный id: "))
    end_id = int(input("конечный id: "))
    if start_id > end_id:
        end_id = start_id
    books_data = get_books_all_data(start_id, end_id)
    save_books_data(books_data)


def get_books_all_data(start_id, end_id):
    '''Функция использует курсор базы данных для выполнения SQL-запроса,
    который выбирает все строки из таблицы books_all с id в заданном диапазоне.
    Результат представляет собой список кортежей, где каждый кортеж содержит данные одной строки таблицы. '''
    with connections['database_books'].cursor() as cursor:
        cursor.execute("SELECT * FROM books_all WHERE id BETWEEN %s AND %s", [start_id, end_id])
        columns = [col[0] for col in cursor.description]
        books_data = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return books_data


def save_books_data(books_data):
    '''Загрузка новых данных из 'db_old' '''
    i = 0  # счетчик итераций
    ii = 0  # счетчик успешных итераций
    iii = 0  # счетчик необработанных исключений
    n = 0  # счетчик пропущенных итераций

    for i, book_data in enumerate(books_data):
        try:
            # Проверяем уникальность id_old
            if ModelBooks.objects.filter(id_old=book_data['id']).exists():
                n += 1
                # print(f"Книга с id_old: {book_data['id']} уже зарегистрирована, пропускаем...")
                continue
            # Проверяем наличие торрент-файла
            elif book_data['torrent'] is None:
                n += 1
                print(f"Для книги с id_old: {book_data['id']} нет торрент-файла, пропускаем...")
                continue
            # Проверяем наличие картинки
            elif book_data['picture'] is None:
                n += 1
                print(f"Для книги с id_old: {book_data['id']} нет загруженной картинки, пропускаем...")
                continue

            # Проверяем и создаем связанных авторов
            authors = book_data.get('author', '').split(', ')
            # from django.core.exceptions import ObjectDoesNotExist
            author_instances = []
            for author_name in authors:
                author_slug = translit_re(author_name)  # Генерируем слаг автора
                try:
                    # Пытаемся найти автора по слагу
                    A = Author.objects.get(slug=author_slug)
                    # Если есть экземпляр модели с таким слагом.
                    author = A.name  # Запомним имя (name) зафиксированное в модели 'Author'
                except ObjectDoesNotExist:
                    # Если автор не найден, приводим имя к требуемому виду
                    author = author_name.title()  # Первую букву каждого слова переводит в верхний регистр, а все остальные в нижний
                try:
                    # Ищем или создаем автора в модели 'Author'
                    author_instance, created = Author.objects.get_or_create(name=author)
                    author_instances.append(author_instance)
                except Exception as e:
                    # Обрабатываем другие возможные исключения, если они возникнут
                    iii += 1  # счетчик необработанных исключений
                    print(f"Ошибка обработки автора: {author_name}: {e}")

            # Проверяем и создаем связанных чтецов
            readers = book_data.get('reading', '').split(', ')
            # from django.core.exceptions import ObjectDoesNotExist
            reader_instances = []
            for reader_name in readers:
                reader_slug = translit_re(reader_name)   # Генерируем слаг чтеца
                try:
                    # Пытаемся найти чтеца по слагу
                    R = Reader.objects.get(slug=reader_slug)
                    # Если есть экземпляр модели с таким слагом.
                    reader = R.name  # Запомним имя зафиксированное в модели 'Reader'
                except ObjectDoesNotExist:
                    # Если чтец не найден, приводим имя к требуемому виду
                    reader = reader_name.title()  # Первую букву каждого слова переводит в верхний регистр, а все остальные в нижний
                try:
                    # Ищем или создаем чтеца в модели 'Reader'
                    reader_instance, created = Reader.objects.get_or_create(name=reader)
                    reader_instances.append(reader_instance)
                except Exception as e:
                    # Обрабатываем другие возможные исключения, если они возникнут
                    iii += 1  # счетчик необработанных исключений
                    print(f"Ошибка обработки чтеца: {reader_name}: {e}")

            # Проверяем и создаем связанный цикл
            cycle_name = book_data.get('cycle', '')
            if not cycle_name:
                cycle_instance = None
            else:
                cycle_slug = translit_re(cycle_name)
                # Пытаемся найти цикл по слагу
                try:
                    cycle_instance = Cycle.objects.get(slug=cycle_slug)
                    # Если цикл найден, обновляем его имя, если оно отличается
                    if cycle_instance.name != cycle_name:
                        cycle_instance.name = cycle_name
                        cycle_instance.save()
                except Cycle.DoesNotExist:
                    # Если цикла с таким слагом нет, создаем новый
                    cycle_instance = Cycle.objects.create(name=cycle_name, slug=cycle_slug)

            # Проверяем и создаем связанные жанры
            subcats = book_data.get('genre', '').split(', ')
            subcat_instances = []

            for subcat_name in subcats:
                subcat_slug = f'{translit_re(subcat_name)}'  # Генерируем слаг Жанра

                try:
                    # Пытаемся найти жанр по слагу
                    subcat_instance = ModelSubcategories.objects.get(slug=subcat_slug)
                    # Если есть экземпляр модели с таким слагом, добавляем его в список
                    subcat_instances.append(subcat_instance)

                except ObjectDoesNotExist:
                    try:
                        # Если жанра нет, создаем новый и присваиваем категорию "Другое"
                        other_category, _ = ModelCategories.objects.get_or_create(name="Другое")
                        # Приводим имя к требуемому виду
                        subcat_name_capitalized = subcat_name.capitalize()
                        # Создаем экземпляр ModelSubcategories
                        new_subcat = ModelSubcategories.objects.create(name=subcat_name_capitalized,
                                                                      category=other_category)
                        # Добавляем новый жанр в список
                        subcat_instances.append(new_subcat)

                    except IntegrityError as e:
                        # Обрабатываем ошибку уникальности (если такой жанр был создан другим потоком в то время,
                        # как мы его искали или создавали)
                        # В этом случае, снова пытаемся найти уже созданный жанр
                        genre_instance = ModelSubcategories.objects.get(slug=subcat_slug)
                        subcat_instances.append(genre_instance)

                    except Exception as e:
                        # Обрабатываем другие возможные исключения, если они возникнут
                        iii += 1  # счетчик необработанных исключений
                        print(f"Ошибка обработки `жанра`: {subcat_name}: {e}")


            # Генерируем путь к торрент-файлу
            path_torrent = f"files_torrent/{book_data['path_torrent']}/{book_data['torrent']}"
            # Генерируем путь к картинке
            path_picture = f"files_picture/{book_data['path_torrent']}/{book_data['picture']}"

            # Создаем экземпляр ModelBooks
            book_instance = ModelBooks.objects.create(
                id_old=book_data['id'],
                title=book_data['title'],
                # Генерируем уникальный слаг для заголовка и авторов
                slug=f"{translit_re(book_data['title'])}-{translit_re(book_data['author'])}",
                year=book_data["year"],
                duration=book_data['duration'],
                quality=book_data['quality'],
                number_in_cycle=book_data['number_cycle'],
                size=book_data['size'],
                description=book_data['description'],
                subdirectory=book_data['path_torrent'],
                torrent=path_torrent,
                picture=path_picture,
                like=book_data['like'],
                dislike=book_data['dislike'],
                total_comments=book_data['comments'],
                cycle=cycle_instance,
            )

            # Сохраняем объект ModelBooks, чтобы получить id
            book_instance.save()

            # Добавляем связанных авторов, чтецов и жанры
            book_instance.authors.set(author_instances)
            book_instance.readers.set(reader_instances)
            book_instance.book_subcategories.set(subcat_instances)

            ii += 1  # счетчик успешных итераций
            print(f"{ii} / {i + 1} ({iii}) | Book with id_old {book_data['id']} successfully saved.")
        except Exception as e:
            iii += 1  # счетчик необработанных исключений
            print(f"{ii} / {i + 1} ({iii}) | Error saving book with id_old {book_data['id']}: {e}")

    print(f'Всего успешно обработано {ii} из {i + 1} записей.')
    print(f'В том числе необработанных исключений {iii} из {i + 1} записей')
    print(f'Пропущено при обработке {n} записей')

if __name__ == "__main__":
    main()