# D:\Python\myProject\bookshelves\app\audiobooks\admin.py

from django.contrib import admin
from .models import Author, Reader, Cycle, ModelSubcategories, ModelBooks, ModelCategories


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
    list_display = ('title', 'slug', 'year', 'is_published')
    prepopulated_fields = {'slug': ('title',)}

    filter_horizontal = ('authors', 'readers', 'book_subcategories')
    ordering = ('pk',)  # 'pk' - это порядок регистрации


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
