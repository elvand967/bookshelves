# D:\Python\myProject\bookshelves\app\audiobooks\templatetags\audiobooks_tags.py

from django import template
from django.urls import reverse
from ..models import ModelCategories, ModelSubcategories

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
                'url': reverse('category_books', args=[category.slug])  # assuming you have a URL named 'category_books'
            },
            'subcategories': []
        }
        subcategories = ModelSubcategories.objects.filter(category=category)

        for subcategory in subcategories:
            category_data['subcategories'].append({
                'name': subcategory.name,
                'slug': subcategory.slug,
                'url': reverse('subcategory_books', args=[category.slug, subcategory.slug])  # assuming you have URLs for subcategories
            })

        menu_data.append(category_data)
    return {'menu_data': menu_data, 'cat_selected': cat_selected, 'subcat_selected': subcat_selected}
