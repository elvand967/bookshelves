# D:\Python\myProject\bookshelves\app\(p)downloading_cat_subcat.py

# Служебные утилиты
import os
from django import setup
# Устанавливаем переменную окружения, указывающую Django, в каком проекте искать настройки
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
# Настраиваем Django
setup()

from audiobooks.models import ModelSubcategories, ModelCategories


def main():
    # Первичная загрузка категорий и жанров
    populate_categories_and_subcategories()


def populate_categories_and_subcategories():
    '''Первичная загрузка категорий и жанров'''
    # Категории
    categories = [
        "Аудиоспектакль",
        "Бизнес и обучение",
        "Биографии и мемуары",
        "Боевики, детективы и триллеры",
        "Здоровье и медицина",
        "Мистика и ужасы",
        "Наука и познавательная литература",
        "Семейные и детские",
        "Классика",
        "Фантастика",
        "Философия",
        "Фэнтези",
        "Альтернативные истории и любовь",
        "Эзотерика и религия",
        "Другое",
    ]

    for category_name in categories:
        category = ModelCategories.objects.create(name=category_name)
        print(f"Добавлена категория: {category}")

    # Подкатегории
    subcategories_mapping = {
        "Аудиоспектакль": ["Аудиоспектакль"],
        "Бизнес и обучение": ["Бизнес", "Обучение"],
        "Биографии и мемуары": ["Биографии", "Мемуары"],
        "Боевики, детективы и триллеры": ["Боевик", "Боевики", "Детектив", "Детективы", "Триллер", "Триллеры"],
        "Здоровье и медицина": ["Медицина", "Здоровье", "Психология"],
        "Мистика и ужасы": ["Мистика", "Ужасы"],
        "Наука и познавательная литература": [
            "На иностранных языках",
            "Научно-популярное",
            "Познавательная литература",
            "История",
        ],
        "Семейные и детские": [
            "Для детей",
            "Приключения",
            "Сказка", "Сказки",
            "Семейные",
            "Юмор",
            "Сатира",
        ],
        "Классика": ["Классика", "Поэзия", "Проза", "Роман"],
        "Фантастика": [
            "Попаданцы",
            "Этногенез",
            "Технотьма",
            "Фантастика",
            "Метро 2033",
            "Постапокалипсис",
            "EVE online",
            "S.T.A.L.K.E.R.",
            "Warhammer 40000",
            "LitRPG",
            "S-T-I-K-S",
        ],
        "Философия": ["Философия"],
        "Фэнтези": ["Любовное фэнтези", "Фэнтези"],
        "Альтернативные истории и любовь": ["Любовный роман", "Альтернативная история"],
        "Эзотерика и религия": ["Эзотерика", "Религия"],
    }

    for category_name, subcategory_names in subcategories_mapping.items():
        category = ModelCategories.objects.get(name=category_name)
        for subcategory_name in subcategory_names:
            subcategory = ModelSubcategories.objects.create(
                category=category, name=subcategory_name
            )
            print(f"Добавлена подкатегория: {subcategory}")


if __name__ == "__main__":
    main()