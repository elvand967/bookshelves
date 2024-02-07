# D:\Python\myProject\bookshelves\app\audiobooks\forms.py

from django import forms
from audiobooks.models import ModelSubcategories


class ContactForm(forms.Form):
    title = forms.CharField(label='Тема', max_length=255,
                            widget=forms.TextInput(attrs={'placeholder': 'Тема сообщения'}))
    subcat = forms.ModelChoiceField(label='Жанр',queryset=ModelSubcategories.objects.all(), required=False)
    content = forms.CharField(label='Сообщение',
                              widget=forms.Textarea(attrs={'placeholder': 'Ваше сообщение', 'rows': 8}))
    is_published = forms.BooleanField(label='Опубликовать в FAG', required=False)

    # Поля для незарегистрированных пользователей
    name = forms.CharField(label='Имя', max_length=255, required=False,
                           widget=forms.TextInput(attrs={'placeholder': 'Ваше Имя'}))
    email = forms.EmailField(label='Email', required=False, widget=forms.EmailInput(attrs={'placeholder': 'Ваш E-mail'}))