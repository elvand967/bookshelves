# D:\Python\myProject\bookshelves\app\rating\templatetags\rating_tags.py

from django import template
from rating.models import AverageRating

register = template.Library()

@register.inclusion_tag('rating/templatetags/ratings_preview.html')
def show_ratings_preview(book_ids):
    try:
        rating_preview = AverageRating.objects.get(book_id=book_ids)
    except AverageRating.DoesNotExist:
        rating_preview = None

    talent_ind = float(rating_preview.talent) * 10 if rating_preview else 0
    plot_ind = float(rating_preview.plot) * 10 if rating_preview else 0
    voice_ind = float(rating_preview.voice) * 10 if rating_preview else 0

    ratings = {
        'rating_preview': rating_preview,
        'talent_ind': talent_ind,
        'plot_ind': plot_ind,
        'voice_ind': voice_ind,
    }
    return ratings


# сортировка по рейтингам
@register.inclusion_tag('rating/templatetags/sort_menu.html', takes_context=True)
def sort_menu(context, cat_selected=None, subcat_selected=None):
    sort_fields = [
        {'field': 'plot', 'label': 'Сюжет'},
        {'field': 'talent', 'label': 'Талант'},
        {'field': 'voice', 'label': 'Голос'},
    ]

    return {'sort_fields': sort_fields, 'cat_selected': cat_selected, 'subcat_selected': subcat_selected}
