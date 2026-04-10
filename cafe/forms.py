from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from .models import CustomUser, Visitors
import re


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        }),
        label='Пароль'
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Подтвердите пароль'
        }),
        label='Подтвердить пароль'
    )

    class Meta:
        model = Visitors
        fields = ['username', 'first_name', 'last_name', 'phone']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите логин'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите имя'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите фамилию'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+7 (999) 123-45-67'
            }),
        }
        labels = {
            'username': 'Логин',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'phone': 'Телефон',
        }

    def clean_login(self):
        """Валидация логина"""
        username = self.cleaned_data.get('username')
        if Visitors.objects.filter(username=username).exists():
            raise ValidationError('Пользователь с таким логином уже существует')
        if len(username) < 3:
            raise ValidationError('Логин должен содержать минимум 3 символа')
        return username


    def clean_password(self):
        """Валидация пароля"""
        password = self.cleaned_data.get('password')
        if len(password) < 6:
            raise ValidationError('Пароль должен содержать минимум 6 символов')
        return password


    def clean_phone(self):
        """Валидация телефона"""
        phone = self.cleaned_data.get('phone')
        # Удаляем все нецифровые символы для проверки
        phone_clean = re.sub(r'\D', '', phone)

        if len(phone_clean) < 10:
            raise ValidationError('Введите корректный номер телефона')

        # Проверяем уникальность телефона
        if CustomUser.objects.filter(phone=phone).exists():
            raise ValidationError('Пользователь с таким телефоном уже зарегистрирован')

        return phone


    def clean(self):
        """Общая валидация формы"""
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise ValidationError('Пароли не совпадают')

        return cleaned_data


    def save(self, commit=True):
        """Сохранение пользователя с хешированием пароля"""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])

        if commit:
            try:
                user.save()
            except Exception as e:
                raise ValidationError(f'Ошибка данных: {str(e)}')

        return user

class CustomLoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login': 'Неверное имя пользователя или пароль.',
        'inactive': 'Этот аккаунт неактивен.',
    }
    class Meta:
        model = Visitors
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите логин'
            }),
            'password': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите пароль'
            }),
        }
        labels = {
            'username': 'Логин',
            'password': 'Пароль',
        }

