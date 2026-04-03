# models.py


from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    # Добавляем поле телефон, если нужно
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.username

#setings
AUTH_USER_MODEL = 'myapp.CustomUser'

# forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Логин',
            'id': 'username'
        }),
        label='Логин'
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Пароль',
            'id': 'password'
        }),
        label='Пароль'
    )

    # Добавляем поле "Запомнить меня"
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Запомнить меня'
    )

    error_messages = {
        'invalid_login': 'Неверный логин или пароль',
        'inactive': 'Аккаунт деактивирован',
    }


# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.urls import reverse
from .forms import LoginForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')  # Перенаправляем на главную, если уже авторизован

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            remember_me = form.cleaned_data.get('remember_me')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

                # Настройка сессии для "Запомнить меня"
                if not remember_me:
                    request.session.set_expiry(0)  # Сессия закроется при закрытии браузера
                else:
                    request.session.set_expiry(1209600)  # 2 недели

                # Перенаправление на следующую страницу или главную
                next_url = request.GET.get('next', 'home')
                return redirect(next_url)
            else:
                messages.error(request, 'Неверный логин или пароль')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

< !-- templates / login.html -->
< !DOCTYPE
html >
< html
lang = "ru" >
< head >
< meta
charset = "UTF-8" >
< meta
name = "viewport"
content = "width=device-width, initial-scale=1.0" >
< title > Авторизация < / title >
< link
href = "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
rel = "stylesheet" >
< style >
body
{
    background: linear - gradient(135deg,  # 667eea 0%, #764ba2 100%);
min - height: 100
vh;
display: flex;
align - items: center;
justify - content: center;
}
.login - card
{
    background: white;
border - radius: 15
px;
box - shadow: 0
10
px
40
px
rgba(0, 0, 0, 0.1);
padding: 40
px;
width: 100 %;
max - width: 450
px;
}
.login - header
{
    text - align: center;
margin - bottom: 30
px;
}
.login - header
h2
{
    color:  # 333;
        font - weight: 600;
}
.btn - login
{
    background: linear - gradient(135deg,  # 667eea 0%, #764ba2 100%);
border: none;
width: 100 %;
padding: 12
px;
font - size: 16
px;
font - weight: 600;
margin - top: 20
px;
}
.btn - login: hover
{
    transform: translateY(-2px);
box - shadow: 0
5
px
15
px
rgba(0, 0, 0, 0.2);
}
.form - control: focus
{
    border - color:  # 667eea;
        box - shadow: 0
0
0
0.2
rem
rgba(102, 126, 234, 0.25);
}
< / style >
    < / head >
        < body >
        < div


class ="login-card" >

< div


class ="login-header" >

< h2 > Вход
в
систему < / h2 >
< p


class ="text-muted" > Введите ваши учетные данные < / p >

< / div >

{ % if messages %}
{ %
for message in messages %}
< div


class ="alert alert-{{ message.tags }} alert-dismissible fade show" role="alert" >


{{message}}
< button
type = "button"


class ="btn-close" data-bs-dismiss="alert" > < / button >

< / div >
{ % endfor %}
{ % endif %}

< form
method = "post"
action = "{% url 'login' %}" >
{ % csrf_token %}

< div


class ="mb-3" >

< label
for ="username" class ="form-label" > Логин < / label >
{{form.username}}
{ % if form.username.errors %}
< div


class ="text-danger small" > {{form.username.errors}} < / div >


{ % endif %}
< / div >

< div


class ="mb-3" >

< label
for ="password" class ="form-label" > Пароль < / label >
{{form.password}}
{ % if form.password.errors %}
< div


class ="text-danger small" > {{form.password.errors}} < / div >


{ % endif %}
< / div >

< div


class ="mb-3 form-check" >


{{form.remember_me}}
< label


class ="form-check-label" for ="remember_me" >


Запомнить
меня
< / label >
< / div >

< button
type = "submit"


class ="btn btn-primary btn-login" >


Войти
< / button >
< / form >

< div


class ="text-center mt-4" >

< a
href = "{% url 'password_reset' %}"


class ="text-decoration-none" > Забыли пароль? < / a >

< br >
< span


class ="text-muted" > Нет аккаунта? < / span >

< a
href = "{% url 'register' %}"


class ="text-decoration-none" > Зарегистрироваться < / a >

< / div >
< / div >

< script
src = "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js" > < / script >
< / body >
< / html >


# urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('home/', views.home_view, name='home'),  # Главная страница после входа
]


# settings.py
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'login'

# Для сообщений
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}

# decorators.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

# Использование в views.py:
@login_required(login_url='login')
def home_view(request):
    return render(request, 'home.html', {'user': request.user})


# views.py (альтернатива)
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .forms import LoginForm


class CustomLoginView(LoginView):
    authentication_form = LoginForm
    template_name = 'login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')

    def form_invalid(self, form):
        messages.error(self.request, 'Неверный логин или пароль')
        return super().form_invalid(form)

    # Создание виртуального окружения
    python - m
    venv
    venv
    source
    venv / bin / activate  # Linux/Mac
    # или
    venv\Scripts\activate  # Windows

    # Установка Django
    pip
    install
    django

    # Создание проекта
    django - admin
    startproject
    myproject
    cd
    myproject

    # Создание приложения
    python
    manage.py
    startapp
    accounts

    # Миграции
    python
    manage.py
    makemigrations
    python
    manage.py
    migrate

    # Создание суперпользователя
    python
    manage.py
    createsuperuser

    # Запуск сервера
    python
    manage.py
    runserver




