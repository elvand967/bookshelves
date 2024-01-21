# D:\Python\myProject\bookshelves\app\audiobooks\templatetags\rating_tags.py

from django import template
from django.urls import reverse
from ..models import ModelCategories, ModelSubcategories, ModelBooks


register = template.Library()

@register.inclusion_tag('audiobooks/templatetags/menu_catsubcat.html', name='my_menu_catsubcat')
def menu_catsubcat(cat_selected=None, subcat_selected=None):
    categories = ModelCategories.objects.all()
    menu_data = [{
        'category': {
            'name': 'Все жанры',
            'slug': 'vse_zhanry',
            'url': reverse('home')
        },
        'subcategories': []
    }]

    for category in categories:
        category_data = {
            'category': {
                'name': category.name,
                'slug': category.slug,
                'url': reverse('cat', args=[category.slug])  # assuming you have a URL named 'cat'
            },
            'subcategories': []
        }

        subcategories = ModelSubcategories.objects.filter(category=category)

        for subcategory in subcategories:
            category_data['subcategories'].append({
                'name': subcategory.name,
                'slug': subcategory.slug,
                'url': reverse('subcat', args=[subcategory.slug])
            })

        menu_data.append(category_data)

    return {'menu_data': menu_data, 'cat_selected': cat_selected, 'subcat_selected': subcat_selected}






@register.inclusion_tag('audiobooks/templatetags/book_slider.html', name='book_slider')
def book_slider():
    # Получаем 18 случайных объектов ModelBooks с изображениями
    books_with_images = ModelBooks.objects.exclude(picture=None).order_by('?')[:12]
    # print(books_with_images)
    return {'books_with_images': books_with_images}


# @register.inclusion_tag('audiobooks/ratings_preview.html')
# def show_ratings_preview(book_ids):
#     books = ModelBooks.objects.filter(id__in=book_ids).select_related('average_rating')
#
#     for book in books:
#         # Добавление вычисляемых полей к словарю average_rating каждой книги
#         book.average_rating.talent_ind = float(book.average_rating.talent) * 10
#         book.average_rating.plot_ind = float(book.average_rating.plot) * 10
#         book.average_rating.voice_ind = float(book.average_rating.voice) * 10
#
#     return {'books': books}