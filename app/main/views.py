# D:\Python\myProject\bookshelves\app\main\views.py
from django.http import HttpResponseNotFound
from django.shortcuts import render

from main.forms import ContactForm


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
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
    else:
        form = ContactForm()

    data = {
        'title': 'Обратная связь',
        'form': form,
    }
    return render(request, 'main/feedback.html', context=data)


def chat(request):
    data = {
        'title': 'Общий чат',
        'text': 'Общий чат сайта',
    }
    return render(request, 'main/chat.html', context=data)


