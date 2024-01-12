# D:\Python\myProject\bookshelves\app\audiobooks\views.py
# from django.core.paginator import Paginator
# from django.shortcuts import render
# from .models import ModelBooks
#
# from itertools import groupby
#
# def index(request, category_slug=None, subcategory_slug=None):
#     cat_selected = 'vse_zhanry'
#     subcat_selected = None
#
#     books = ModelBooks.objects.prefetch_related('book_subcategories', 'authors', 'readers').all()
#
#     if category_slug:
#         books = books.filter(book_subcategories__category__slug=category_slug)
#         cat_selected = category_slug
#
#     if subcategory_slug:
#         books = books.filter(book_subcategories__slug=subcategory_slug)
#         cat_selected = category_slug
#         subcat_selected = subcategory_slug
#
#     paginator = Paginator(books, 10)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#
#     # Группировка по id книги
#     grouped_books = {key: list(group) for key, group in groupby(books, key=lambda x: x.id)}
#
#
#
#
#     data = {
#         'title': 'Аудиокниги с книжной полки',
#         'books': [groups[0] for groups in grouped_books.values()],
#         'cat_selected': cat_selected,
#         'subcat_selected': subcat_selected,
#         'page_obj': page_obj,
#     }
#     return render(request, 'audiobooks/index.html', context=data)

from django.core.paginator import Paginator
from django.shortcuts import render
from .models import ModelBooks
from django.db.models import Q

def index(request, category_slug=None, subcategory_slug=None):
    cat_selected = 'vse_zhanry'
    subcat_selected = None

    books = ModelBooks.objects.prefetch_related('book_subcategories', 'authors', 'readers').all()

    if category_slug:
        books = books.filter(book_subcategories__category__slug=category_slug)
        cat_selected = category_slug

    if subcategory_slug:
        books = books.filter(book_subcategories__slug=subcategory_slug)
        cat_selected = category_slug
        subcat_selected = subcategory_slug

    # Группировка по id книги
    grouped_books = (
        ModelBooks.objects
        .filter(id__in=books.values_list('id', flat=True))
        .prefetch_related('book_subcategories', 'authors', 'readers')
        .distinct()
    )

    paginator = Paginator(grouped_books, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    data = {
        'title': 'Аудиокниги с книжной полки',
        'books': page_obj,
        'cat_selected': cat_selected,
        'subcat_selected': subcat_selected,
        'page_obj': page_obj,
    }
    return render(request, 'audiobooks/index.html', context=data)
