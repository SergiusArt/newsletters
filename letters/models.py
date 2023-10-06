from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from unidecode import unidecode

NULLABLE = {'blank': True, 'null': True}


# Модель клиента
# Контактный email | Ф.И.О. | Комментарий
class Client(models.Model):
    email = models.EmailField(verbose_name='Почта')
    full_name = models.CharField(max_length=255, verbose_name='Полное имя')
    comment = models.TextField(blank=True, verbose_name='Комментарии')

    def __str__(self):
        return self.full_name

    # Мета данные: отображаемые имена моделей
    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


# Модель рассылки
# Время рассылки| Периодичность (раз в день, в неделю, в месяц) | Статус рассылки (завершена, создана, запущена)
class Newsletter(models.Model):
    TIME_CHOICES = (
        ('daily', 'Раз в день'),
        ('weekly', 'Раз в неделю'),
        ('monthly', 'Раз в месяц')
    )

    STATUS_CHOICES = (
        ('created', 'Создана'),
        ('started', 'Запущена'),
        ('completed', 'Завершена')
    )

    send_time = models.DateTimeField(verbose_name='Время рассылки')
    frequency = models.CharField(max_length=10, choices=TIME_CHOICES, verbose_name='Периодичность')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name='Статус', default='Создана')
    name = models.CharField(max_length=255, verbose_name='Наименование', default='Новая рассылка')
    message = models.ForeignKey('Message', on_delete=models.SET_NULL, **NULLABLE, verbose_name='Сообщение')

    def __str__(self):
        return self.name

    # Мета данные: отображаемые имена моделей
    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


# Модель сообщения
# Тема письма | Тело письма
class Message(models.Model):
    subject = models.CharField(max_length=255, verbose_name='Тема письма')
    body = models.TextField(verbose_name='Тело письма')

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


# Модель с логами рассылки
# Дата и время последней рассылки | Статус попытки | Ответ почтового сервера (если он был)
class MailLog(models.Model):
    newsletter = models.ForeignKey(Newsletter, on_delete=models.CASCADE, verbose_name='Рассылка', **NULLABLE)
    last_sent = models.DateTimeField(verbose_name='Дата и время последней рассылки')
    status = models.CharField(max_length=100, verbose_name='Статус попытки')
    server_response = models.CharField(max_length=255, **NULLABLE, verbose_name='Ответ почтового сервера')

    def __str__(self):
        return f"Mail Log {self.last_sent}"

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'
