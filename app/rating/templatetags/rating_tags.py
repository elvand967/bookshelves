# D:\Python\myProject\bookshelves\app\rating\templatetags\rating_tags.py

from django import template
from django.urls import reverse

from rating.mixins import SortingMixin
from rating.models import AverageRating

register = template.Library()


@register.inclusion_tag('rating/templatetags/ratings_preview.html')
def show_ratings_preview(book_ids):
    try:
        rating_preview = AverageRating.objects.get(book_id=book_ids)
    except AverageRating.DoesNotExist:
        rating_preview = None

    plot_ind = float(rating_preview.plot) * 10 if rating_preview else 0
    talent_ind = float(rating_preview.talent) * 10 if rating_preview else 0
    voice_ind = float(rating_preview.voice) * 10 if rating_preview else 0

    ratings = {
        'rating_preview': rating_preview,
        'plot_ind': plot_ind,
        'talent_ind': talent_ind,
        'voice_ind': voice_ind,
    }
    return ratings


# сортировка по рейтингам
# @register.inclusion_tag('rating/templatetags/sort_menu.html', takes_context=True)
# def sort_menu(context, cat_selected=None, subcat_selected=None, sort_reiting=None):
#     if cat_selected == 'None':
#         cat_selected = None
#
#     if subcat_selected == 'None':
#         subcat_selected = None
#
#     sort_ratings = [
#         {'rating': 'plot', 'label': 'Сюжет', 'class_i': 'icon-people-robbery'},
#         {'rating': 'talent', 'label': 'Писательский талант', 'class_i': 'icon-pen-to-square'},
#         {'rating': 'voice', 'label': 'Качество озвучивания', 'class_i': 'icon-microphone-lines'},
#     ]
#
#     for element in sort_ratings:
#         if sort_reiting is not None:
#             # Активный статус рейтинга
#             if sort_reiting.lstrip('-').lower() == element['rating'].lower():
#                 # Определяем направление сортировки
#                 # Если sort_reiting начинается с '-'
#                 if sort_reiting.startswith('-'):
#                     # У нас активный рейтинг со знаком '-'
#                     element.update({'active_rating': '-1', })
#                 else:
#                     element.update({'active_rating': '1', })
#             else:
#                 # здесь зафиксируем неактивный рейтинг
#                 element.update({'active_rating': '0', })
#         else:
#             # зафиксируем все неактивные рейтинги
#             element.update({'active_rating': '0', })
#
#         # Формируем исходный url для сброса
#         if subcat_selected is not None:
#             element.update({
#                 'condition_url': reverse('subcat', args=[subcat_selected])})
#         else:
#             element.update({
#                 'condition_url': reverse('cat', args=[cat_selected])})
#
#         # url направлений сортировки
#         element.update({
#             'asc_url': reverse('sorted_index', args=[cat_selected, subcat_selected, element['rating']]),
#             'desc_url': reverse('sorted_index', args=[cat_selected, subcat_selected, f'-{element["rating"]}']),
#         })
#
#     return {'sort_ratings': sort_ratings, 'sort_reiting': sort_reiting}


# @register.inclusion_tag('rating/templatetags/sort_menu.html', takes_context=True)
# def sort_menu(context, cat_selected=None, subcat_selected=None, active_rating=None):
#     # Инициализируем объект SortingMixin
#     sorting_mixin = SortingMixin()
#
#     if cat_selected == 'None':
#         cat_selected = None
#
#     if subcat_selected == 'None':
#         subcat_selected = None
#
#     # Используем методы SortingMixin для генерации контекста
#     sort_menu_context = sorting_mixin.get_sort_menu_context(cat_selected, subcat_selected, active_rating)
#
#     return sort_menu_context
