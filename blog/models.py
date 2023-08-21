from django.conf import settings
from django.db import models

from clients.models import NULLABLE


# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=50, verbose_name='Заголовок')
    view_count = models.IntegerField(default=0, verbose_name='Просмотры')
    content = models.TextField(**NULLABLE, verbose_name='Содержимое')
    image = models.ImageField(upload_to='blogs/', **NULLABLE, verbose_name='Превью')
    published = models.DateTimeField(db_index=True, auto_now_add=True, verbose_name='Дата создания')
    email = models.EmailField(max_length=100, verbose_name='Электронная почта', unique=True)
    user_blog = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE,
                                  verbose_name='пользователь')

    def __str__(self):
        return f'{self.title}. Просмотров ({self.view_count})'

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'
        ordering = ('-published',)
