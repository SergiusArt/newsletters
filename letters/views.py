from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, ListView, DetailView

from letters.models import Newsletter, Client, Message, MailLog


# Главная страница
class LettersView(TemplateView):
    template_name = 'letters/index.html'
    extra_context = {
        'title': 'Общая информация о сайте'
    }


# Страница с рассылками
class NewsletterListView(ListView):
    model = Newsletter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# Страница редактирования рассылки
class NewsletterUpdateView(UpdateView):
    model = Newsletter
    fields = ['send_time', 'frequency', 'status', 'name', 'message']
    template_name = 'letters/newsletter_form.html'
    success_url = reverse_lazy('letters:newsletter')


# Страница добавления рассылки
class NewsletterCreateView(CreateView):
    model = Newsletter
    fields = ['send_time', 'frequency', 'status', 'name', 'message']
    template_name = 'letters/newsletter_form.html'
    success_url = reverse_lazy('letters:newsletter')


# Страница с клиентами
class ClientListView(ListView):
    model = Client
    template_name = 'letters/client_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# Страница редактирования клиента
class ClientUpdateView(UpdateView):
    model = Client
    fields = ['email', 'full_name', 'comment']
    template_name = 'letters/client_form.html'
    success_url = reverse_lazy('letters:clients')


# Страница добавления клиента
class ClientCreateView(CreateView):
    model = Client
    fields = ['email', 'full_name', 'comment']
    template_name = 'letters/client_form.html'
    success_url = reverse_lazy('letters:clients')


# Страница с сообщениями
class MessageListView(ListView):
    model = Message
    template_name = 'letters/message_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# Страница редактирования сообщения
class MessageUpdateView(UpdateView):
    model = Message
    fields = ['subject', 'body']
    template_name = 'letters/message_form.html'
    success_url = reverse_lazy('letters:message')


# Страница добавления сообщения
class MessageCreateView(CreateView):
    model = Message
    fields = ['subject', 'body']
    template_name = 'letters/message_form.html'
    success_url = reverse_lazy('letters:message')


# Страница детального просмотра сообщения
class MessageDetailView(DetailView):
    model = Message
    template_name = 'letters/message_detail.html'
    context_object_name = 'message'


# Страница с логами
class MailLogListView(ListView):
    model = MailLog
    template_name = 'letters/maillog_list.html'
    context_object_name = 'logs'

    def get_queryset(self):
        queryset = super().get_queryset()
        newsletter_id = self.kwargs.get('pk')
        return queryset.filter(newsletter_id=newsletter_id)

