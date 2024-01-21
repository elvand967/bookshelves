# D:\Python\myProject\bookshelves\app\audiobooks\views.py

from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Case, When, F, Value, IntegerField, Q

from audiobooks.models import ModelBooks, ModelSubcategories


def index(request, category_slug=None, subcategory_slug=None, sort_reiting=None):
    if subcategory_slug == 'none':
        subcategory_slug = None

    cat_selected = 'vse_zhanry'
    subcat_selected = None

    if sort_reiting is None:
        if category_slug is None and subcategory_slug is None:
            # Нет фильтров, выбираем все книги
            condition = None

        elif category_slug is not None and subcategory_slug is None:
            # Выбираем книги заданной категории
            condition = Q(book_subcategories__category__slug=category_slug)
            cat_selected = category_slug

        elif subcategory_slug is not None and category_slug is None:
            # Выбираем книги заданной подкатегории
            condition = Q(book_subcategories__slug=subcategory_slug)
            # Получаем информацию о подкатегории
            subcategory_info = ModelSubcategories.objects.get(slug=subcategory_slug)
            cat_selected = subcategory_info.category.slug
            subcat_selected = subcategory_slug

        # Применяем фильтр
        base_books = ModelBooks.objects.only('id', 'book_subcategories', 'authors', 'readers',
                                                 'average_rating').filter(condition)

    else:
        #  Фильтруем книги по категории и/или подкатегории для дальнейшей сортировки
        if category_slug == 'vse_zhanry':
            condition = None

        else:
            # Используем Q объекты для построения условия
            condition = Q(book_subcategories__category__slug=category_slug)
            if subcategory_slug:
                # используем `&` для логического И (AND)
                condition &= Q(book_subcategories__slug=subcategory_slug)

        # Применяем фильтр
        base_books = ModelBooks.objects.only('id', 'book_subcategories', 'authors', 'readers',
                                             'average_rating').select_related('average_rating').filter(condition)

        cat_selected = category_slug
        subcat_selected = subcategory_slug

    # Группировка по id книги
    grouped_books = (
        base_books
        .filter(id__in=base_books.values_list('id', flat=True))
        .prefetch_related('book_subcategories', 'authors', 'readers', 'average_rating')
        .distinct()
    )

    # Проверка наличия условия сортировки
    # Используем `average_rating__{sort_reiting}` для обращения к полю связанной модели
    if sort_reiting:
        # Определяем направление сортировки
        if sort_reiting.startswith('-'):
            # Если sort_reiting начинается с '-', убираем его и добавляем '-' перед полем
            sort_field = f'-average_rating__{sort_reiting[1:]}'
        else:
            # Иначе, добавляем поле напрямую
            sort_field = f'average_rating__{sort_reiting}'

        # Применяем сортировку
        grouped_books = grouped_books.order_by(sort_field)

    # Реализуем пагинацию
    paginator = Paginator(grouped_books, 9)
    # paginator = Paginator(base_books, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    data = {
        'title': 'Аудиокниги с книжной полки',
        'page_obj': page_obj,
        'cat_selected': cat_selected,
        'subcat_selected': subcat_selected,
        'sort_reiting': sort_reiting,
    }

    return render(request, 'audiobooks/index.html', context=data)
