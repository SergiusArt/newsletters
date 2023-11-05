# Импортируем необходимые библиотеки
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, DetailView
from django.db.models import Q
from blog.models import Blog
from blog.views import is_content_manager, is_manager
from letters.models import Newsletter, Client, Message, MailLog
from django.shortcuts import get_object_or_404


# Главная страница
class LettersView(TemplateView):
    # Указываем шаблон и контекст
    template_name = 'letters/index.html'
    extra_context = {
        'title': 'Добро пожаловать на сайт рассылок!'
    }

    # Получаем данные для отображения на странице
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_newsletters'] = Newsletter.objects.count()
        context['active_newsletters'] = Newsletter.objects.exclude(Q(status='off')).count()
        context['client_count'] = Client.objects.values('email').distinct().count()
        context['blogs'] = Blog.objects.order_by('?')[:3]
        context['is_content_manager'] = is_content_manager(self.request.user)
        context['is_manager'] = is_manager(self.request.user)
        return context


# Страница с рассылками
class NewsletterListView(LoginRequiredMixin, ListView):
    model = Newsletter

    # Получаем список рассылок
    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_superuser or self.request.user.is_staff:
            return qs
        return qs.filter(owner=self.request.user)

    # Получаем контекст для отображения на странице
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_content_manager'] = is_content_manager(self.request.user)
        context['is_manager'] = is_manager(self.request.user)
        if self.request.user.is_superuser or self.request.user.is_staff:
            context['is_staff'] = True
        return context

    # Обрабатываем POST запрос
    def post(self, request, *args, **kwargs):
        if 'status_off' in request.POST:
            newsletter_id = request.POST.get('status_off')
            newsletter = get_object_or_404(Newsletter, id=newsletter_id)
            newsletter.status = 'off'
            newsletter.save()
        elif 'status_on' in request.POST:
            newsletter_id = request.POST.get('status_on')
            newsletter = get_object_or_404(Newsletter, id=newsletter_id)
            newsletter.status = 'created'
            newsletter.save()
        return self.get(request, *args, **kwargs)


# Страница редактирования рассылки
class NewsletterUpdateView(LoginRequiredMixin, UpdateView):
    model = Newsletter
    fields = ['send_time', 'frequency', 'name', 'message', 'emails']
    template_name = 'letters/newsletter_form.html'
    success_url = reverse_lazy('letters:newsletter')

    # Получаем форму для редактирования
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['emails'].queryset = Client.objects.filter(owner=self.request.user)
        form.fields['message'].queryset = Message.objects.filter(owner=self.request.user)
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_content_manager'] = is_content_manager(self.request.user)
        context['is_manager'] = is_manager(self.request.user)
        return context


# Страница добавления рассылки
class NewsletterCreateView(LoginRequiredMixin, CreateView):
    model = Newsletter
    fields = ['send_time', 'frequency', 'name', 'message', 'emails']
    template_name = 'letters/newsletter_form.html'
    success_url = reverse_lazy('letters:newsletter')

    # Проверяем валидность формы
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    # Получаем форму для добавления
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['emails'].queryset = Client.objects.filter(owner=self.request.user)
        form.fields['message'].queryset = Message.objects.filter(owner=self.request.user)
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_content_manager'] = is_content_manager(self.request.user)
        context['is_manager'] = is_manager(self.request.user)
        return context


# Страница с клиентами
class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'letters/client_list.html'

    # Получаем список клиентов
    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_superuser or self.request.user.is_staff:
            return qs
        return qs.filter(owner=self.request.user)

    # Получаем контекст для отображения на странице
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_content_manager'] = is_content_manager(self.request.user)
        context['is_manager'] = is_manager(self.request.user)
        return context


# Страница редактирования клиента
class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    fields = ['email', 'full_name', 'comment']
    template_name = 'letters/client_form.html'
    success_url = reverse_lazy('letters:clients')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_content_manager'] = is_content_manager(self.request.user)
        context['is_manager'] = is_manager(self.request.user)
        return context


# Страница добавления клиента
class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    fields = ['email', 'full_name', 'comment']
    template_name = 'letters/client_form.html'
    success_url = reverse_lazy('letters:clients')

    # Проверяем валидность формы
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_content_manager'] = is_content_manager(self.request.user)
        context['is_manager'] = is_manager(self.request.user)
        return context


# Страница с сообщениями
class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'letters/message_list.html'

    # Получаем список сообщений
    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_superuser or self.request.user.is_staff:
            return qs
        return qs.filter(owner=self.request.user)

    # Получаем контекст для отображения на странице
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_content_manager'] = is_content_manager(self.request.user)
        context['is_manager'] = is_manager(self.request.user)
        return context


# Страница редактирования сообщения
class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    fields = ['subject', 'body']
    template_name = 'letters/message_form.html'
    success_url = reverse_lazy('letters:message')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_content_manager'] = is_content_manager(self.request.user)
        context['is_manager'] = is_manager(self.request.user)
        return context


# Страница добавления сообщения
class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    fields = ['subject', 'body']
    template_name = 'letters/message_form.html'
    success_url = reverse_lazy('letters:message')

    # Проверяем валидность формы
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_content_manager'] = is_content_manager(self.request.user)
        context['is_manager'] = is_manager(self.request.user)
        return context


# Страница детального просмотра сообщения
class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = 'letters/message_detail.html'
    context_object_name = 'message'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_content_manager'] = is_content_manager(self.request.user)
        context['is_manager'] = is_manager(self.request.user)
        return context


# Страница с логами
class MailLogListView(LoginRequiredMixin, ListView):
    model = MailLog
    template_name = 'letters/maillog_list.html'
    context_object_name = 'logs'

    # Получаем список логов
    def get_queryset(self):
        queryset = super().get_queryset()
        newsletter_id = self.kwargs.get('pk')
        return queryset.filter(newsletter_id=newsletter_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_content_manager'] = is_content_manager(self.request.user)
        context['is_manager'] = is_manager(self.request.user)
        return context


