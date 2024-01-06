# D:\Python\myProject\bookshelves\app\audiobooks\urls.py

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),         # http://127.0.0.1:8000/
    path('category/<slug:category_slug>/', views.index, name='category_books'),
    path('category/<slug:category_slug>/subcategory/<slug:subcategory_slug>/', views.index, name='subcategory_books'),
]


# Добавляем путь для просмотра медиафайлов только в режиме отладки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)