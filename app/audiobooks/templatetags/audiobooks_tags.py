# D:\Python\myProject\bookshelves\app\audiobooks\templatetags\audiobooks_tags.py


from django.shortcuts import get_object_or_404
from django import template
from django.urls import reverse
from ..models import ModelCategories, ModelSubcategories, ModelBooks

register = template.Library()


'''Встраиваемый пользовательский тег вертикального меню категорий/подкатегориый'''
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


'''Встраиваемый пользовательский тег слайдера-кольца'''
@register.inclusion_tag('audiobooks/templatetags/ring_slider_books.html', name='ring_slider_books')
def book_slider():
    # Получаем 12 случайных объектов ModelBooks с изображениями
    books_with_images = ModelBooks.objects.exclude(picture=None).order_by('?')[:12]
    # print(books_with_images)
    return {'books_with_images': books_with_images}


'''Встраиваемый пользовательский тег пагинатора'''
@register.inclusion_tag('audiobooks/templatetags/pagination.html', name='pagination')
def custom_pagination(page_obj):
    return {'page_obj': page_obj}


'''Встраиваемый пользовательский тег блока поиска'''
@register.inclusion_tag('audiobooks/templatetags/search_tag.html')
def search_tag():
    # data = [
    #     {
    #         "type": "text",
    #         "name": "title",
    #         "placeholder": "название книги",
    #     },
    #     {
    #         "type": "text",
    #         "name": "cycle",
    #         "placeholder": "название цикла",
    #     },
    #     {
    #         "type": "text",
    #         "name": "author",
    #         "placeholder": "имя и/или фамилию автора",
    #     },
    #     {
    #         "type": "text",
    #         "name": "reader",
    #         "placeholder": "имя и/или фамилию чтеца",
    #     },
    #     {
    #         "type": "text",
    #         "name": "on_all",
    #         "placeholder": "строку, для общего поиска",
    #     },
    # ]
    # return {'data': data}
    return {}


# @register.simple_tag
# def breadcrumbs(cat_selected=None, subcat_selected=None):
#     if subcat_selected:
#         subcategory = get_object_or_404(ModelSubcategories, slug=subcat_selected)
#         return f'Книжная полка "{subcategory.name}"'
#
#     elif cat_selected:
#         if cat_selected == 'vse_zhanry':
#             return 'Все жанры'
#         else:
#             category = get_object_or_404(ModelCategories, slug=cat_selected)
#             return f'Книжный шкаф "{category.name}"'
#
#     return 'Все жанры'  # или любой другой дефолтный текст



# @register.simple_tag
# def breadcrumbs(cat_selected=None, subcat_selected=None, search_query=None):
#     if search_query:
#         return f'Результат поиска `{search_query}`'
#
#     if subcat_selected:
#         subcategory = get_object_or_404(ModelSubcategories, slug=subcat_selected)
#         return f'Книжная полка "{subcategory.name}"'
#
#     elif cat_selected:
#         if cat_selected == 'vse_zhanry':
#             return 'Все жанры'
#         else:
#             category = get_object_or_404(ModelCategories, slug=cat_selected)
#             return f'Книжный шкаф "{category.name}"'
#
#     return 'Все жанры'  # или любой другой дефолтный текст

@register.simple_tag
def breadcrumbs(cat_selected=None, subcat_selected=None, search_query=None, search_results_count=None):
    if search_query:
        if search_results_count is not None:
            if search_results_count == 0:
                return f'По запросу "{search_query}" нет записей'
            else:
                return f'По запросу "{search_query}" найдено {search_results_count} записей'
        else:
            return f'Результаты по запросу "{search_query}"'

    elif subcat_selected:
        subcategory = get_object_or_404(ModelSubcategories, slug=subcat_selected)
        return f'Книжная полка "{subcategory.name}"'

    elif cat_selected:
        if cat_selected == 'vse_zhanry':
            return 'Все жанры'
        else:
            category = get_object_or_404(ModelCategories, slug=cat_selected)
            return f'Книжный шкаф "{category.name}"'

    return 'Все жанры'  # или любой другой дефолтный текст




