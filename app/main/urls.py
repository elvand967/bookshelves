# D:\Python\myProject\bookshelves\app\main\urls.py

from django.urls import path

from . import views



urlpatterns = [
    # path('', views.index, name='home'),         # http://127.0.0.1:8000/
    path('about/', views.about, name='about'),  # http://127.0.0.1:8000/about/
    path('fag/', views.fag, name='fag'),        # http://127.0.0.1:8000/fag/
    path('feedback/', views.feedback, name='feedback'),  # http://127.0.0.1:8000/feedback/
    path('chat/', views.chat, name='chat'),     # http://127.0.0.1:8000/chat/
]
