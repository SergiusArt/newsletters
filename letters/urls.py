from django.urls import path

from letters.apps import LettersConfig
from letters.views import LettersView, NewsletterListView, ClientListView, MessageListView, MailLogListView, \
    ClientUpdateView, ClientCreateView, NewsletterCreateView, NewsletterUpdateView, MessageCreateView, \
    MessageUpdateView, MessageDetailView

app_name = LettersConfig.name

# url адресация в приложении
urlpatterns = [
    path('', LettersView.as_view(), name='index'),
    path('newsletter/', NewsletterListView.as_view(), name='newsletter'),
    path('newsletter/create/', NewsletterCreateView.as_view(), name='newsletter_create'),
    path('newsletter/<int:pk>/edit/', NewsletterUpdateView.as_view(), name='newsletter_update'),

    path('clients/', ClientListView.as_view(), name='clients'),
    path('clients/<int:pk>/edit/', ClientUpdateView.as_view(), name='clients_update'),
    path('clients/create/', ClientCreateView.as_view(), name='clients_create'),

    path('message/', MessageListView.as_view(), name='message'),
    path('message/create/', MessageCreateView.as_view(), name='message_create'),
    path('message/<int:pk>/edit/', MessageUpdateView.as_view(), name='message_update'),
    path('message/<int:pk>/view/', MessageDetailView.as_view(), name='message_view'),

    # path('maillog/', MailLogListView.as_view(), name='maillog'),
    path('maillog/<int:pk>/', MailLogListView.as_view(), name='maillog'),
]