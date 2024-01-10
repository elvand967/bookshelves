# D:\Python\myProject\bookshelves\app\audiobooks\admin.py

from django.contrib import admin
from .models import Author, Reader, Cycle, ModelSubcategories, ModelBooks, ModelCategories
from django.utils.safestring import mark_safe

@admin.register(ModelCategories)
class ModelCategoriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('pk',)  # 'pk' - это порядок регистрации


@admin.register(ModelSubcategories)
class ModelSubcategoriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'category')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('pk',)  # 'pk' - это порядок регистрации


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('pk',)  # 'pk' - это порядок регистрации


@admin.register(ModelBooks)
class ModelBooksAdmin(admin.ModelAdmin):
    list_display = ('book_picture', 'title', 'slug', 'year', 'is_published')
    prepopulated_fields = {'slug': ('title',)}

    filter_horizontal = ('authors', 'readers', 'book_subcategories')
    ordering = ('pk',)  # 'pk' - это порядок регистрации

    @admin.display(description="Изображение", ordering='content')
    def book_picture(self, book: ModelBooks):
        if book.picture:
            return mark_safe(f"<img src='{book.picture.url}' width=50>")
        return "Без фото"


@admin.register(Cycle)
class CycleAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('pk',)  # 'pk' - это порядок регистрации


@admin.register(Reader)
class ReaderAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('pk',)  # 'pk' - это порядок регистрации


admin.site.site_header = 'Книжные полки'
admin.site.site_title = 'Аудиокниги, скачать торрентом'
