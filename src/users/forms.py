from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import AdminUser


class AdminUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = AdminUser
        fields = ('username', 'service_group')


class AdminUserChangeForm(UserChangeForm):
    class Meta:
        model = AdminUser
        fields = ('username', 'service_group')
