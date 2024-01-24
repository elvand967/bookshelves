# D:\Python\myProject\bookshelves\app\main\templatetags\main_tags.py

from django import template
from django.template.defaultfilters import safe

register = template.Library()


@register.simple_tag(name="horizontal_menu")
def get_horizontal_menu():
    """Функция def get_horizontal_menu(), которая будет возвращать
    список ссылок главного меню при вызове нашего тега из шаблона.
    Свяжем эту функцию с тегом, или, превратим эту функцию в тег,
    используя специальный декоратор
    `@register.simple_tag(name='horizontal_menu')`,
     доступный через переменную `register`."""
    menu = [
        {
            "title": "Главная",
            "url_name": "home",
            "link_hint": "Аудиокниги с книжной полки",
        },
        {
            "title": "О нас",
            "url_name": "about",
            "link_hint": "О нас, контакты, другая информация",
        },
        {"title": "FAG", "url_name": "fag", "link_hint": "Часто задаваемые вопросы"},
        {
            "title": "Обратная связь",
            "url_name": "feedback",
            "link_hint": "Отправить сообщение администрации сайта",
        },
        {"title": "Чат", "url_name": "chat", "link_hint": "Войти в общий чат сайта"},
    ]
    # menu = ["О сайте", "Добавить книгу", "Обратная связь", "Войти"]
    return menu


@register.simple_tag(name="menu_users")
def get_users_menu(user):
    """Функция def get_users_menu(), которая будет возвращать
    список ссылок входа, регистрации, профиля и выхода пользователя
    при вызове нашего тега из шаблона.
    Свяжем эту функцию с тегом, или, превратим эту функцию в тег, используя специальный декоратор
    `@register.simple_tag(name='menu_users')`,
     доступный через переменную `register`."""
    # user = request.user
    if user.is_authenticated:
        menu = [
            {
                "title": "Профиль",
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


@register.inclusion_tag('main/templatetags/pagination.html', name='pagination')
def custom_pagination(page_obj):
    return {'page_obj': page_obj}



# @register.inclusion_tag('main/templatetags/pagination.html', name='pagination')
# def custom_pagination(page_obj):
#     return {'page_obj': page_obj}


# @register.simple_tag
# def custom_pagination(page_obj, query_params):
#     paginator = page_obj.paginator
#     current_page = page_obj.number
#
#     html = '<div class="paginate"><ul>'
#
#     if page_obj.has_previous():
#         html += f'<li><a href="?{query_params}page=1">&lang;&lang;</a></li>'
#         html += f'<li><a href="?{query_params}page={current_page - 1}">&lang;</a></li>'
#
#     for p in paginator.page_range:
#         html += f'<li><a href="?{query_params}page={p}">{p}</a></li>'
#
#     if page_obj.has_next():
#         html += f'<li><a href="?{query_params}page={current_page + 1}">&rang;</a></li>'
#         html += f'<li><a href="?{query_params}page={paginator.num_pages}">&rang;&rang;</a></li>'
#
#     html += '</ul></div>'
#     return html


