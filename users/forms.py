# Импорт необходимых модулей
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from users.models import User


# Форма регистрации пользователя
class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


# Форма профиля пользователя
class UserProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'avatar', 'country')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Скрываем поле пароля
        self.fields['password'].widget = forms.HiddenInput()
