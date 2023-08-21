from django.db import models

NULLABLE = {'blank': True, 'null': True}


# Create your models here.
class Client(models.Model):
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    middle_name = models.CharField(max_length=50, verbose_name='Отчество')
    email = models.EmailField(max_length=50, unique=True, verbose_name='Электронный адрес')
    comment = models.TextField(**NULLABLE, max_length=500, verbose_name='Комментарий')
    client_user = models.ForeignKey('users.User', on_delete=models.SET_NULL, verbose_name='пользователь', **NULLABLE)

    def __str__(self):
        return f'{self.last_name} {self.first_name} ({self.email})'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ('last_name', 'first_name', 'middle_name')
