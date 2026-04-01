from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class Client(models.Model):
    # Поля аутентификации
    login = models.CharField(max_length=150, unique=True, verbose_name='Логин')
    password = models.CharField(max_length=128, verbose_name='Пароль')

    # Личная информация
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')

    # Контактная информация
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Телефон должен быть в формате: +999999999. До 15 цифр."
    )
    phone = models.CharField(
        validators=[phone_regex],
        max_length=17,
        verbose_name='Телефон'
    )

    # Системные поля
    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='Баланс'
    )
    status = models.IntegerField(
        default=0,
        verbose_name='Статус',
        help_text='0 - обычный, 1 - VIP, 2 - администратор'
    )
    orders_count = models.IntegerField(
        default=0,
        verbose_name='Количество заказов'
    )

    # Поля для отслеживания
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.login})"

    def set_password(self, raw_password):
        """Хеширование пароля"""
        from django.contrib.auth.hashers import make_password
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """Проверка пароля"""
        from django.contrib.auth.hashers import check_password
        return check_password(raw_password, self.password)


