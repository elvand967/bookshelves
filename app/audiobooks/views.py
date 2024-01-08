# D:\Python\myProject\bookshelves\app\audiobooks\views.py

from django.shortcuts import render
from .models import ModelBooks

from itertools import groupby

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
    grouped_books = {key: list(group) for key, group in groupby(books, key=lambda x: x.id)}

    data = {
        'title': 'Аудиокниги с книжной полки',
        'books': [groups[0] for groups in grouped_books.values()],
        'cat_selected': cat_selected,
        'subcat_selected': subcat_selected,
    }
    return render(request, 'audiobooks/index.html', context=data)