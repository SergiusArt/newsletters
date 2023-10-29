from django.db import models
from src.constants import NULLABLE


class Blog(models.Model):
    # Название блога
    title = models.CharField(max_length=100, verbose_name='Название')

    # Содержание блога
    content = models.TextField(verbose_name='Содержание', **NULLABLE)

    # Изображение блога
    image = models.ImageField(upload_to='blog_images/', verbose_name='Изображение', **NULLABLE)

    # Количество просмотров блога
    views = models.IntegerField(default=0, verbose_name='Количество просмотров')

    # Дата публикации блога
    published_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'
