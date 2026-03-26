# from django.contrib.auth.models import AbstractUser
# from django.db import models
#
# class CustomUser(AbstractUser):
#     position = models.CharField(max_length=50)   # должность
#
#     def __str__(self):
#         return self.username
#
#     class Meta:
#         verbose_name_plural = "Пользователь"
#
#
# class Staff(CustomUser):
#     wage = models.CharField(max_length=50)       # З.П.
#
#     class Meta:
#         verbose_name_plural = "Сотрудник"
#
# class Visitors(CustomUser):
#     count = models.IntegerField(default=0, verbose_name='количество посещений')
#     last_visit = models.IntegerField(default=0, verbose_name='последнее посещение', null=True, blank=True)
#
#     class Meta:
#         verbose_name_plural = "Посетитель"
#
