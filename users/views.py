from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView

from blog.views import is_content_manager, is_manager
from src.functions import send_mail, generate_password
from users.forms import UserRegisterForm, UserProfileForm
from users.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


# Класс для регистрации пользователя
class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:verify_email')

    def form_valid(self, form):
        response = super().form_valid(form)
        email = form.cleaned_data['email']
        # Получаем код верификации из базы данных пользователя
        verification_code = f"Ваш код верификации: {User.objects.get(email=email).verification_code}"
        send_mail(email, 'Код подтверждения', verification_code)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_content_manager'] = is_content_manager(self.request.user)
        context['is_manager'] = is_manager(self.request.user)
        return context


# Класс для обновления профиля пользователя
class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    # Получение объекта пользователя
    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_content_manager'] = is_content_manager(self.request.user)
        context['is_manager'] = is_manager(self.request.user)
        return context


# Функция для вывода страницы с одним полем для подтверждения верификации пользователя
def verify_email(request):
    if request.method == 'POST':
        verification_code = request.POST.get('verification_code')

        try:
            user = User.objects.get(verification_code=verification_code)
            if user.verification_code == verification_code:
                user.is_active = True
                user.is_verified = True
                user.save()
                return redirect('users:login')
        except User.DoesNotExist:
            messages.error(request, 'Неверный код верификации')

    return render(request, 'users/verify_email.html')


# Функция для восстановления пароля пользователя
def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)
            new_password = generate_password(length=10)

            # Перезаписываем пароль пользователя
            user.set_password(new_password)
            user.save()

            new_password_text = f'Ваш новый пароль:\n{new_password}'
            # Отправляем письмо с новым паролем пользователя
            send_mail(email, 'Восстановление пароля', new_password_text)
            return redirect('users:login')
        except User.DoesNotExist:
            messages.error(request, 'Неверный email')

    return render(request, 'users/recover_password.html')


# Класс для отображения списка пользователей
class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = 'users/user_list.html'

    def test_func(self):
        return is_manager(self.request.user)

    def post(self, request, *args, **kwargs):
        user_id = request.POST.get('block_user')

        try:
            # Блокируем пользователя
            user = User.objects.get(id=user_id)
            user.is_active = False
            user.save()
        except User.DoesNotExist:
            pass

        user_id = request.POST.get('unlock_user')

        try:
            # Разблокируем пользователя
            user = User.objects.get(id=user_id)
            user.is_active = True
            user.save()
        except User.DoesNotExist:
            pass

        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_content_manager'] = is_content_manager(self.request.user)
        context['is_manager'] = is_manager(self.request.user)
        return context

