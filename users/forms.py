from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from users.models import User
from django import forms


class UserRegisterForm(UserCreationForm):
    """Форма для регистрации пользователя"""
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class UserProfileForm(UserChangeForm):
    """Форма для редактирования профиля пользователя"""
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'avatar', 'phone')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()


class UserStatusForm(UserChangeForm):
    """Форма для управления статусом пользователя"""
    class Meta:
        model = User
        fields = ('is_active',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()

