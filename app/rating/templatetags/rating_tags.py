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
