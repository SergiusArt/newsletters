from django.contrib import admin

from letters.models import Client, Newsletter, Message, MailLog


# Отображение клиентов в админке
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'comment')
    verbose_name_plural = 'Клиенты'


# Отображение рассылок в админке
@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('send_time', 'frequency', 'status')
    verbose_name_plural = 'Рассылки'


# Отображение сообщений в админке
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'body')
    verbose_name_plural = 'Сообщения'


# Отображение логов в админке
@admin.register(MailLog)
class MailLogAdmin(admin.ModelAdmin):
    list_display = ('newsletter', 'last_sent', 'status', 'server_response')
    verbose_name_plural = 'Логи'

