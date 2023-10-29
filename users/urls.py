# Импортирование необходимых модулей
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from users.views import RegisterView, ProfileView, verify_email, reset_password, UserListView
from users.apps import UsersConfig

# Установка имени приложения
app_name = UsersConfig.name

# Определение URL-шаблонов
urlpatterns = [
    # URL для входа в систему
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),

    # URL для выхода из системы
    path('logout/', LogoutView.as_view(), name='logout'),

    # URL для регистрации
    path('register/', RegisterView.as_view(), name='register'),

    # URL для профиля пользователя
    path('profile/', ProfileView.as_view(), name='profile'),

    # URL для подтверждения почты пользователя
    path('verify-email/', verify_email, name='verify_email'),

    # URL для сброса пароля пользователя
    path('reset-password/', reset_password, name='reset_password'),

    # URL для просмотра списка пользователей
    path('users/', UserListView.as_view(), name='user_list'),
]
