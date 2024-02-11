# D:\Python\myProject\bookshelves\app\audiobooks\views.py
from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic import ListView
from django.db.models import Q

from audiobooks.mixins import SortingMixin
from audiobooks.models import ModelBooks, ModelSubcategories, ModelCategories


def test(request):
    data = {
        'title': 'test',
        'text': 'Тестова страница сайта',
    }
    return render(request, 'audiobooks/test.html', context=data)


"""Превью книг по категориям/подкатегориям + сортировка по критериям"""
class BookListView(SortingMixin, ListView):
    model = ModelBooks
    template_name = "audiobooks/index.html"
    paginate_by = 9  # Количество книг на странице

    def normalize_none(self, value):
        """Преобразуем строку 'None' в None."""
        return None if value == "None" else value

    def get_queryset(self):
        category_slug = self.normalize_none(self.kwargs.get("category_slug"))
        subcategory_slug = self.normalize_none(self.kwargs.get("subcategory_slug"))
        active_rating = self.normalize_none(self.kwargs.get("active_rating"))

        if (
            category_slug is None or category_slug == "vse_zhanry"
        ) and subcategory_slug is None:
            # Нет фильтров, выбираем все книги
            condition = Q()

        elif category_slug is not None and subcategory_slug is None:
            # Выбираем книги заданной категории
            condition = Q(book_subcategories__category__slug=category_slug)

        elif subcategory_slug is not None:
            # Выбираем книги заданной подкатегории
            condition = Q(book_subcategories__slug=subcategory_slug)

        base_books = (
            ModelBooks.objects.only(
                "id", "book_subcategories", "authors", "readers", "average_rating"
            )
            .filter(condition)
            .distinct()
        )

        # Применяем сортировку с использованием миксина
        base_books = self.apply_sorting(base_books, active_rating)

        return base_books

    def get_context_data(self, **kwargs):
        category_slug = self.normalize_none(self.kwargs.get("category_slug"))
        subcategory_slug = self.normalize_none(self.kwargs.get("subcategory_slug"))
        active_rating = self.normalize_none(self.kwargs.get("active_rating"))
        context = super().get_context_data(**kwargs)

        if subcategory_slug is not None:
            # Получаем информацию от подкатегории о ее категории
            subcategory_info = ModelSubcategories.objects.get(slug=subcategory_slug)
            cat_sel = subcategory_info.category.slug
            subcat_sel = subcategory_slug

        elif category_slug is None and subcategory_slug is None:
            cat_sel = "vse_zhanry"
            subcat_sel = None

        else:
            cat_sel = category_slug
            subcat_sel = subcategory_slug

        context["cat_sel"] = cat_sel
        context["subcat_sel"] = subcat_sel
        context["active_rating"] = active_rating

        # Получаем контекст для меню сортировки с использованием миксина
        sort_menu_context = self.get_sort_menu_context(
            cat_sel, subcat_sel, active_rating
        )
        context.update(sort_menu_context)

        return context


"""Поиск книг по полям: Название; Цикл; Автор; Чтец + общий поиск"""
class SearchResultsView(ListView):
    model = ModelBooks
    template_name = "audiobooks/index.html"
    paginate_by = 9

    def normalize_none(self, value):
        """Преобразуем строку 'None' в None."""
        return None if value == "None" else value

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            base_books = ModelBooks.objects.filter(
                Q(title__icontains=query)
                | Q(description__icontains=query)
                | Q(cycle__name__icontains=query)
                | Q(authors__name__icontains=query)
                | Q(readers__name__icontains=query)
            ).distinct()
        else:
            base_books = ModelBooks.objects.all()

        # Сохраняем результаты поиска в атрибуте объекта
        self.search_results = base_books
        return base_books

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q", "")
        context["title"] = "Поиск"
        context["cat_sel"] = ("vse_zhanry",)
        context["subcat_sel"] = (None,)
        context["sort_reiting"] = None
        # Используем результаты поиска из атрибута объекта
        context["search_results_count"] = (
            self.search_results.count() if hasattr(self, "search_results") else 0
        )
        return context


class AudioBookDetailView(View):
    template_name = "audiobooks/audiobook_detail.html"

    def get(self, request, slug):
        audiobook = get_object_or_404(ModelBooks, slug=slug)
        return render(request, self.template_name, {"audiobook": audiobook})
