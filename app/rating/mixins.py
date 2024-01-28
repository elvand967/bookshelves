# D:\Python\myProject\bookshelves\app\rating\mixins.py

from django.urls import reverse
from rating.models import AverageRating


class SortingMixin:
    # def get_reset_url(self, cat_selected, subcat_selected, field):
    #     if subcat_selected is not None:
    #         return reverse('subcat', args=[subcat_selected])
    #     else:
    #         return reverse('cat', args=[cat_selected])

    def get_sort_menu_context(self, cat_selected, subcat_selected, active_rating):
        sort_ratings = [
            {'rating': 'plot', 'label': 'Сюжет', 'active': 'No', 'class_i': 'icon-people-robbery'},
            {'rating': 'talent', 'label': 'Писательский талант', 'active': 'No', 'class_i': 'icon-pen-to-square'},
            {'rating': 'voice', 'label': 'Качество озвучивания', 'active': 'No', 'class_i': 'icon-microphone-lines'},
        ]

        ar = ''
        if active_rating is not None:
            # Есть активированный рейтинг.
            ar = active_rating.lstrip('-').lower()

        for item in sort_ratings:
            if item['rating'] == ar:
                # Определяем направление сортировки
                item.update({'active': 'down', }) if active_rating.startswith(
                    '-') else item.update({'active': 'up', })

            # Формируем исходный url для сброса
            if subcat_selected:
                item.update({'condition_url': reverse('subcat', args=[subcat_selected])})
            else:
                if cat_selected is None:
                    item.update({'condition_url': reverse('home')})
                else:
                    item.update({'condition_url': reverse('cat', args=[cat_selected])})

            # url направлений сортировки
            item.update({
                'asc_url': reverse('sorted_index', args=[cat_selected, subcat_selected, item['rating']]),
                'desc_url': reverse('sorted_index', args=[cat_selected, subcat_selected, f'-{item["rating"]}']),
            })

        return {'sort_ratings': sort_ratings, 'active_rating': active_rating}

    def apply_sorting(self, base_books, active_rating):
        if active_rating:
            # Определяем направление сортировки
            sort_field = f'-average_rating__{active_rating[1:]}' if active_rating.startswith(
                '-') else f'average_rating__{active_rating}'

            # Применяем сортировку
            base_books = base_books.order_by(sort_field)

        return base_books
