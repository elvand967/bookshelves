# D:\Python\myProject\bookshelves\app\main\templatetags\users_tags.py

from django import template
from django.template.defaultfilters import safe

register = template.Library()



@register.simple_tag(name="menu_users")
def get_users_menu(user):
    """ Простой пользовательский тег, Функция def get_users_menu(), которая будет возвращать
    список ссылок входа, регистрации, профиля и выхода пользователя
    при вызове нашего тега из шаблона.
    Свяжем эту функцию с тегом, или, превратим эту функцию в тег, используя специальный декоратор
    `@register.simple_tag(name='menu_users')`,
     доступный через переменную `register`."""
    # user = request.user
    if user.is_authenticated:
        menu = [
            {
                "title": user.first_name,
                "url_name": "profile",
                "link_hint": "Профиль пользователя",
            },
            {"title": "Выход", "url_name": "logout", "link_hint": "Выход пользователя"},
        ]
    else:
        menu = [
            {"title": "Вход", "url_name": "login", "link_hint": "Войти на сайт"},
            {
                "title": "Регистрация",
                "url_name": "register",
                "link_hint": "Регистрация на сайте",
            },
        ]

    return menu