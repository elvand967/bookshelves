# D:\Python\myProject\bookshelves\app\audiobooks\urls.py

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='home'),  # http://127.0.0.1:8000/
    path('subcat/<slug:subcategory_slug>/', views.index, name='subcat'),
    path('cat/<slug:category_slug>/', views.index, name='cat'),
    re_path(r'^sort_reiting/(?P<category_slug>[\w-]+)__(?P<subcategory_slug>[\w-]+)__(?P<sort_reiting>[\w-]+)/$',
            views.index, name='sorted_index'),

]

# Добавляем путь для просмотра медиафайлов только в режиме отладки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
