# D:\Python\myProject\bookshelves\app\audiobooks\templatetags\audiobooks_tags.py


from django.shortcuts import get_object_or_404
from django import template
from django.urls import reverse
from ..models import ModelCategories, ModelSubcategories, ModelBooks, AverageRating

register = template.Library()


"""Встраиваемый пользовательский тег вертикального меню категорий/подкатегориый"""
@register.inclusion_tag(
    "audiobooks/templatetags/menu_catsubcat.html", name="my_menu_catsubcat"
)
def menu_catsubcat(cat_sel=None, subcat_sel=None):
    categories = ModelCategories.objects.all()
    menu_data = [
        {
            "category": {
                "name": "Все жанры",
                "slug": "vse_zhanry",
                "url": reverse("home"),
            },
            "subcategories": [],
        }
    ]

    for category in categories:
        category_data = {
            "category": {
                "name": category.name,
                "slug": category.slug,
                "url": reverse(
                    "cat", args=[category.slug]
                ),  # assuming you have a URL named 'cat'
            },
            "subcategories": [],
        }

        subcategories = ModelSubcategories.objects.filter(category=category)

        for subcategory in subcategories:
            category_data["subcategories"].append(
                {
                    "name": subcategory.name,
                    "slug": subcategory.slug,
                    "url": reverse("subcat", args=[subcategory.slug]),
                }
            )

        menu_data.append(category_data)

    return {"menu_data": menu_data, "cat_sel": cat_sel, "subcat_sel": subcat_sel}


"""Встраиваемый пользовательский тег слайдера-кольца"""
@register.inclusion_tag(
    "audiobooks/templatetags/ring_slider_books.html", name="ring_slider_books"
)
def book_slider():
    # Получаем 12 случайных объектов ModelBooks с изображениями
    books_with_images = ModelBooks.objects.exclude(picture=None).order_by("?")[:12]
    # print(books_with_images)
    return {"books_with_images": books_with_images}


"""Встраиваемый пользовательский тег пагинатора"""
@register.inclusion_tag("audiobooks/templatetags/pagination.html", name="pagination")
def custom_pagination(page_obj):
    return {"page_obj": page_obj}


"""Встраиваемый пользовательский тег блока поиска"""
@register.inclusion_tag("audiobooks/templatetags/search_tag.html")
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


""" Заголовок страницы Категория/Подкатегория/уведомление о поиске"""
@register.simple_tag
def breadcrumbs(
    cat_sel=None, subcat_sel=None, search_q=None, search_results_count=None
):
    if search_q:
        if search_results_count is not None:
            if search_results_count == 0:
                return f'По запросу "{search_q}" нет записей'
            else:
                return f'По запросу "{search_q}" найдено {search_results_count} записей'
        else:
            return f'Результаты по запросу "{search_q}"'

    elif subcat_sel:
        subcategory = get_object_or_404(ModelSubcategories, slug=subcat_sel)
        return f'Книжная полка "{subcategory.name}"'

    elif cat_sel:
        if cat_sel == "vse_zhanry":
            return "Все жанры"
        else:
            category = get_object_or_404(ModelCategories, slug=cat_sel)
            return f'Книжный шкаф "{category.name}"'

    return "Все жанры"  # или любой другой дефолтный текст


@register.inclusion_tag('audiobooks/templatetags/ratings_preview.html')
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