from django import forms
from django.core.exceptions import ValidationError
from .models import Client
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
        model = Client
        fields = ['login', 'first_name', 'last_name', 'phone']
        widgets = {
            'login': forms.TextInput(attrs={
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
            'login': 'Логин',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'phone': 'Телефон',
        }

    def clean_login(self):
        """Валидация логина"""
        login = self.cleaned_data.get('login')
        if Client.objects.filter(login=login).exists():
            raise ValidationError('Пользователь с таким логином уже существует')
        if len(login) < 3:
            raise ValidationError('Логин должен содержать минимум 3 символа')
        return login


    def clean_password(self):
        """Валидация пароля"""
        password = self.cleaned_data.get('password')
        if len(password) < 6:
            raise ValidationError('Пароль должен содержать минимум 6 символов')
        if not re.search(r'[A-Za-z]', password):
            raise ValidationError('Пароль должен содержать хотя бы одну букву')
        if not re.search(r'[0-9]', password):
            raise ValidationError('Пароль должен содержать хотя бы одну цифру')
        return password


    def clean_phone(self):
        """Валидация телефона"""
        phone = self.cleaned_data.get('phone')
        # Удаляем все нецифровые символы для проверки
        phone_clean = re.sub(r'\D', '', phone)

        if len(phone_clean) < 10:
            raise ValidationError('Введите корректный    номер телефона')

        # Проверяем уникальность телефона
        if Client.objects.filter(phone=phone).exists():
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
            user.save()
        return user