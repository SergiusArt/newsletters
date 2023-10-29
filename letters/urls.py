# Импортирование необходимых модулей и функций
from django.urls import path
from django.views.decorators.cache import cache_page
from letters.apps import LettersConfig
from letters.views import (
    LettersView,
    NewsletterListView,
    ClientListView,
    MessageListView,
    MailLogListView,
    ClientUpdateView,
    ClientCreateView,
    NewsletterCreateView,
    NewsletterUpdateView,
    MessageCreateView,
    MessageUpdateView,
    MessageDetailView
)

app_name = LettersConfig.name

# Определение маршрутов для приложения
urlpatterns = [
    # Главная страница
    path('', LettersView.as_view(), name='index'),
    
    # Страницы рассылки
    path('newsletter/', cache_page(60)(NewsletterListView.as_view()), name='newsletter'),
    path('newsletter/create/', NewsletterCreateView.as_view(), name='newsletter_create'),
    path('newsletter/<int:pk>/edit/', NewsletterUpdateView.as_view(), name='newsletter_update'),
    
    # Страницы клиентов
    path('clients/', cache_page(60)(ClientListView.as_view()), name='clients'),
    path('clients/<int:pk>/edit/', ClientUpdateView.as_view(), name='clients_update'),
    path('clients/create/', ClientCreateView.as_view(), name='clients_create'),
    
    # Страницы сообщений
    path('message/', cache_page(60)(MessageListView.as_view()), name='message'),
    path('message/create/', MessageCreateView.as_view(), name='message_create'),
    path('message/<int:pk>/edit/', MessageUpdateView.as_view(), name='message_update'),
    path('message/<int:pk>/view/', MessageDetailView.as_view(), name='message_view'),
    
    # Страница журнала почты
    path('maillog/<int:pk>/', MailLogListView.as_view(), name='maillog'),
]
