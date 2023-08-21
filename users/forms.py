from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm, UserChangeForm
from django.forms import models

from clients.forms import StyleMixin
from sender.models import Sender
from users.models import User


class LoginForm(StyleMixin, AuthenticationForm):
    class Meta:
        model = User
        fields = ('email', 'password')


class RegisterUserForm(StyleMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class UserChangePasswordForm(StyleMixin, PasswordChangeForm):
    class Meta:
        model = User


class UserProfileUpdateForm(StyleMixin, UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'avatar', 'password', 'country', 'phone',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()


class ModeratorSenderUpdateForm(StyleMixin, models.ModelForm):
    class Meta:
        model = Sender
        fields = ('status', )
        labels = {'status': 'Текущий статус'}


class ModeratorUserUpdateForm(models.ModelForm):
    class Meta:
        model = User
        fields = ('is_active', )
        labels = {'is_active': 'Статус пользователя'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'custom-control custom-checkbox mb-3'
