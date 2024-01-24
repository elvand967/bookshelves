# D:\Python\myProject\bookshelves\app\audiobooks\views.py

from django.views.generic import ListView
from django.shortcuts import render
# from django.db.models import Case, When, F, Value, IntegerField, Q
from django.db.models import Q

from audiobooks.models import ModelBooks, ModelSubcategories


class BookListView(ListView):
    model = ModelBooks
    template_name = 'audiobooks/index.html'
    paginate_by = 9  # Количество книг на странице

    def normalize_none(self, value):
        """Преобразуем строку 'None' в None."""
        return None if value == 'None' else value

    def get_queryset(self):
        category_slug = self.normalize_none(self.kwargs.get('category_slug'))
        subcategory_slug = self.normalize_none(self.kwargs.get('subcategory_slug'))
        sort_reiting = self.normalize_none(self.kwargs.get('sort_reiting'))

        if (category_slug is None or category_slug == 'vse_zhanry') and subcategory_slug is None:
            # Нет фильтров, выбираем все книги
            condition = Q()

        elif category_slug is not None and subcategory_slug is None:
            # Выбираем книги заданной категории
            condition = Q(book_subcategories__category__slug=category_slug)

        elif subcategory_slug is not None:
            # Выбираем книги заданной подкатегории
            condition = Q(book_subcategories__slug=subcategory_slug)

        base_books = (
            ModelBooks.objects
            .only('id', 'book_subcategories', 'authors', 'readers', 'average_rating')
            .filter(condition)
            .distinct()  # Когда вызывается .distinct(), Django генерирует SQL-запрос с ключевым словом DISTINCT,
            # которое удаляет дубликаты из набора результатов.
        )

        # Проверка наличия условия сортировки
        # Используем `average_rating__{sort_reiting}` для обращения к полю связанной модели
        if sort_reiting:
            # Определяем направление сортировки
            if sort_reiting.startswith('-'):
                # Если sort_reiting начинается с '-', убираем его и добавляем '-' перед полем
                sort_field = f'-average_rating__{sort_reiting[1:]}'
            else:
                # Иначе, добавляем поле напрямую
                sort_field = f'average_rating__{sort_reiting}'

            # Применяем сортировку
            base_books = base_books.order_by(sort_field)

        return base_books

    def get_context_data(self, **kwargs):
        category_slug = self.normalize_none(self.kwargs.get('category_slug'))
        subcategory_slug = self.normalize_none(self.kwargs.get('subcategory_slug'))
        sort_reiting = self.normalize_none(self.kwargs.get('sort_reiting'))
        context = super().get_context_data(**kwargs)

        if subcategory_slug is not None:
            # Получаем информацию от подкатегории о ее категории
            subcategory_info = ModelSubcategories.objects.get(slug=subcategory_slug)
            cat_selected = subcategory_info.category.slug
            subcat_selected = subcategory_slug

        elif category_slug is None and subcategory_slug is None:
            cat_selected = 'vse_zhanry'
            subcat_selected = None

        else:
            cat_selected = category_slug
            subcat_selected = subcategory_slug

        context['cat_selected'] = cat_selected
        context['subcat_selected'] = subcat_selected
        context['sort_reiting'] = sort_reiting

        return context


def search_results(request):
    title = request.GET.get('title', '')
    cycle = request.GET.get('cycle', '')
    author = request.GET.get('author', '')
    reader = request.GET.get('reader', '')

    # Выполните поиск в вашей модели ModelBooks на основе предоставленных параметров

    # Пример:
    books = ModelBooks.objects.filter(
        title__icontains=title,
        cycle__name__icontains=cycle,
        authors__name__icontains=author,
        readers__name__icontains=reader
    )

    context = {'books': books}
    return render(request, 'search_results.html', context)
