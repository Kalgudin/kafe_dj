from django.contrib.auth.models import AbstractUser, User
from django.db import models

class CustomUser(User):
    position = models.CharField(max_length=50)   # должность

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = "Пользователь"


class Staff(CustomUser):
    wage = models.CharField(max_length=50)       # З.П.

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
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='Категория')

    def __str__(self):
        return f"{self.name} - {self.price} руб."

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['category', 'name']


