# D:\Python\myProject\bookshelves\app\main\models.py
from django.db import models

class PageInfo(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    content = models.TextField()

    def __str__(self):
        return self.title
