# D:\Python\myProject\bookshelves\app\audiobooks\views.py

from django.core.paginator import Paginator
from django.shortcuts import render

from rating.models import AverageRating
from .models import ModelBooks
from django.db.models import Q

def index(request, category_slug=None, subcategory_slug=None):
    cat_selected = 'vse_zhanry'
    subcat_selected = None

    # Используем select_related для эффективной загрузки связанных данных
    books = ModelBooks.objects.select_related('average_rating').prefetch_related('book_subcategories', 'authors', 'readers').all()

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
        .select_related('average_rating')  # Добавляем select_related для эффективной загрузки связанных данных
        .prefetch_related('book_subcategories', 'authors', 'readers')
        .distinct()
    )


    paginator = Paginator(grouped_books, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    for book in page_obj.object_list:
        # Добавление вычисляемых полей к словарю average_rating каждой книги
        book.average_rating.talent_ind = float(book.average_rating.talent) * 10
        book.average_rating.plot_ind = float(book.average_rating.plot) * 10
        book.average_rating.voice_ind = float(book.average_rating.voice) * 10

    # Добавление данных AverageRating в контекст
    data = {
        'title': 'Аудиокниги с книжной полки',
        'books': page_obj,
        'cat_selected': cat_selected,
        'subcat_selected': subcat_selected,
        'page_obj': page_obj,
    }

    return render(request, 'audiobooks/index.html', context=data)
