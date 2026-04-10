from django.contrib.auth.models import User
from django.db import models


class CustomUser(User):
    phone = models.CharField(max_length=11, verbose_name='Телефон')
    position = models.CharField(max_length=50)  # должность
    # Поля для отслеживания
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"

    def set_password(self, raw_password):
        """Хеширование пароля"""
        from django.contrib.auth.hashers import make_password
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """Проверка пароля"""
        from django.contrib.auth.hashers import check_password
        return check_password(raw_password, self.password)

    class Meta:
        verbose_name_plural = "Пользователь"
        ordering = ['-created_at']


class Staff(CustomUser):
    wage = models.CharField(max_length=50)  # З.П.

    class Meta:
        verbose_name_plural = "Сотрудник"


class Visitors(CustomUser):
    count = models.IntegerField(default=0, verbose_name='количество посещений')
    last_visit = models.IntegerField(default=0, verbose_name='последнее посещение', null=True, blank=True)

    class Meta:
        verbose_name_plural = "Посетитель"


class Category(models.Model):
    name = models.CharField('Название категории', max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']


class Product(models.Model):
    name = models.CharField('Название продукта', max_length=200)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                # related_name='prods',
                                 verbose_name='Категория')

    def __str__(self):
        return f"{self.name} - {self.price} руб."

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['category', 'name']
