# D:\Python\myProject\bookshelves\app\main\views.py
from django.http import HttpResponseNotFound
from django.shortcuts import render


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

def about(request):
    data = {
        'title': 'О сайте',
        'text': 'На этой странице информация о сайте',
    }
    return render(request, 'main/about.html', context=data)


def fag(request):
    data = {
        'title': 'FAG',
        'text': 'Часто задаваемые вопросы',
    }
    return render(request, 'main/fag.html', context=data)


def feedback(request):
    data = {
        #  'title': 'Обратная связь',  # тестируем отработку 'title' по умолчанию в шаблоне
        'text': 'Здесь должна быть форма обратной связи',
    }
    return render(request, 'main/feedback.html', context=data)


def chat(request):
    data = {
        'title': 'Общий чат',
        'text': 'Общий чат сайта',
    }
    return render(request, 'main/chat.html', context=data)


def login(request):
    data = {
        'title': 'Вход',
        'text': 'Форма входа',
    }
    return render(request, 'main/login.html', context=data)


def logout(request):
    data = {
        'title': 'Выход',
        'text': 'Контролер выхода пользователя',
    }
    return render(request, 'main/logout.html', context=data)


def registeruser(request):
    data = {
        'title': 'Регистрация',
        'text': 'Регистрация пользователя',
    }
    return render(request, 'main/register.html', context=data)


def profile(request):
    data = {
        'title': 'Профиль',
        'text': 'Профиль пользователя',
    }
    return render(request, 'main/profile.html', context=data)