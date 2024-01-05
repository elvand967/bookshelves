# D:\Python\myProject\bookshelves\app\main\admin.py

from django.contrib import admin
from .models import PageInfo
# Use a relative import / Используйте относительный импорт
from .management.commands.backup_copy_db import database_backup

def backup_database(modeladmin, request, queryset):
    database_backup()
# Set a short description for the action / Задайте краткое описание действия
backup_database.short_description = "Резервная копия Database"

class PageInfoAdmin(admin.ModelAdmin):
    # Add the custom action to the model admin / Добавьте настраиваемое действие в администратора модели.
    actions = [backup_database]
# Register your model and its admin / Зарегистрируйте свою модель и ее администратора
admin.site.register(PageInfo, PageInfoAdmin)
