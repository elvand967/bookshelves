# D:\Python\myProject\bookshelves\app\rating\mixins.py

from django.urls import reverse


class SortingMixin:
    def __init__(self, rating_options=None):
        super().__init__()
        self.rating_options = rating_options or [
            {
                "rating": "plot",
                "label": "Сюжет",
                "class_i": "icon-people-robbery",
                "color": "#004242",
            },
            {
                "rating": "talent",
                "label": "Писательский талант",
                "class_i": "icon-pen-to-square",
                "color": "#4169E1",
            },
            {
                "rating": "voice",
                "label": "Качество озвучивания",
                "class_i": "icon-microphone-lines",
                "color": "#BF00FF",
            },
        ]

    def get_sort_menu_context(self, cat_sel, subcat_sel, active_rating):
        """Метод генерирует контекст для меню сортировки с использованием миксина"""
        sort_ratings = []
        # определим статус критерия сортировки
        ar = active_rating.lstrip("-").lower() if active_rating else None

        for item in self.rating_options:
            # регистрируем статус критерия сортировки
            if item["rating"] == ar:
                active = "down" if active_rating.startswith("-") else "up"
            else:
                active = "No"

            # генерируем url ссылки направления сортировки
            condition_url = (
                reverse("subcat", args=[subcat_sel]) if subcat_sel else reverse("home")
            )
            asc_url = reverse(
                "sorted_index", args=[cat_sel, subcat_sel, item["rating"]]
            )
            desc_url = reverse(
                "sorted_index", args=[cat_sel, subcat_sel, f'-{item["rating"]}']
            )

            sort_ratings.append(
                {
                    "rating": item["rating"],
                    "label": item["label"],
                    "class_i": item["class_i"],
                    "color": item["color"],
                    "active": active,
                    "condition_url": condition_url,
                    "asc_url": asc_url,
                    "desc_url": desc_url,
                }
            )

        return {"sort_ratings": sort_ratings, "active_rating": active_rating}

    def apply_sorting(self, base_books, active_rating):
        """Метод обеспечивает сортировку с использованием миксина"""
        if active_rating:
            sort_field = (
                f"-average_rating__{active_rating[1:]}"
                if active_rating.startswith("-")
                else f"average_rating__{active_rating}"
            )
            base_books = base_books.order_by(sort_field)

        return base_books
