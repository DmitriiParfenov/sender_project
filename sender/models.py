from django.db import models

from clients.models import NULLABLE


# Create your models here.
class Sender(models.Model):

    class Period(models.TextChoices):
        DAILY = ('Ежедневно', 'Ежедневно')
        WEEKLY = ('Раз в неделю', 'Раз в неделю')
        MONTHLY = ('Раз в месяц', 'Раз в месяц')
        __empty__ = 'Выбрать'

    class Status(models.TextChoices):
        CREATED = ('создана', 'создана')
        STARTED = ('запущена', 'запущена')
        DONE = ('завершена', 'завершена')
        __empty__ = 'Выбрать'

    subject = models.CharField(max_length=150, verbose_name='Заголовок')
    message = models.TextField(verbose_name='Сообщение')
    client = models.ManyToManyField('clients.Client', verbose_name='Клиент рассылки')
    period = models.CharField(max_length=50, choices=Period.choices, default=Period.DAILY, verbose_name='Периодичность')
    status = models.CharField(max_length=50, choices=Status.choices, default=Status.CREATED, verbose_name='Статус')
    time = models.TimeField(verbose_name='Время')
    sender_user = models.ForeignKey('users.User', on_delete=models.SET_NULL, verbose_name='создатель рассылки',
                                    **NULLABLE)

    def __str__(self):
        return f'{self.subject}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        ordering = ('subject', )
        permissions = [
            (
                'set_disabled',
                'Can disable Рассылка'
            )
        ]


class SenderLog(models.Model):

    class Status(models.TextChoices):
        FAILED = ('Ошибка', 'Ошибка')
        SUCCESS = ('Отправлено', 'Отправлено')

    client = models.ForeignKey('clients.Client', on_delete=models.CASCADE, verbose_name='Клиент')
    sender = models.ForeignKey('sender.Sender', on_delete=models.CASCADE, verbose_name='Рассылка')
    status = models.CharField(max_length=50, choices=Status.choices, default=Status.SUCCESS, verbose_name='Статус')
    last_try = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата последней попытки')

    class Meta:
        verbose_name = 'Информация'
        verbose_name_plural = 'Информации'
