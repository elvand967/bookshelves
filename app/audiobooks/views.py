# D:\Python\myProject\bookshelves\app\audiobooks\views.py

from django.shortcuts import render
from .models import ModelBooks


def index(request, category_slug=None, subcategory_slug=None):
    books = ModelBooks.objects.prefetch_related('book_subcategories', 'authors', 'readers').all()

    cat_selected = 'vse_zhanry'
    subcat_selected = None

    if category_slug:
        books = books.filter(book_subcategories__category__slug=category_slug)
        cat_selected = category_slug

    if subcategory_slug:
        books = books.filter(book_subcategories__slug=subcategory_slug)
        cat_selected = category_slug
        subcat_selected = subcategory_slug

    data = {
        'title': 'Аудиокниги с книжной полки',
        'books': books,
        'cat_selected': cat_selected,
        'subcat_selected': subcat_selected,
    }
    return render(request, 'audiobooks/index.html', context=data)