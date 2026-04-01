from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from .forms import RegistrationForm

def index(request):
    context = {'title': 'Котокафе Мотя',
               'description': '''
    Здесь можно выпить чаю и уютно провести время в
окружении пушистых друзей. А если вы с кем-то из них
по-настоящему подружились - можете усыновить нового
друга в свою семью''',
               'head': 'Добро пожаловать в Кото-кафе "Мотя"!',
               'menu': '''
    <div class="top_menu">
        <a href="/"><div class="selected shadow top_menu_items">Главная</div></a>
        <a href="menu"><div class="shadow top_menu_items">Меню</div></a>
        <a href="contact"><div class="shadow top_menu_items">Контакты</div></a>
    </div>''',
               'center': '''
    <div class="shadow box">
        <img src="static/img/kafe1.jpg"/>
        <p>50+ котиков живут в кото-кафе</p>
    </div>
    <div class="shadow box">
        <p>350+ котиков нашли себе дом</p>
        <img src="static/img/kafe2.jpg"  style="float: right;"/>
    </div>
    <div class="shadow box">
        <img src="static/img/kafe3.jpg"  style="float: right;"/>
        <p>Нашему кафе уже 2 года</p>
    </div>''',
               'bottom': '''
    <div id="Reserve">
        <h2>Бронирование</h2>
    </div>'''}
    return render(request, 'index.html', context)



def menu(request):
    context = {'title': 'Котокафе Мотя', 'description': 'Some Description'}
    return render(request, 'menu.html', context)


def contact(request):
    context = {'title': 'Котокафе Мотя', 'description': 'Some Description'}
    return render(request, 'contact.html', context)


# ////////////////////////////////////////////////////

class RegistrationView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Регистрация успешно завершена! Добро пожаловать, {user.first_name}!')
            return redirect('login')  # Перенаправление на страницу входа   login
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{form.fields[field].label}: {error}')
        return render(request, 'register.html', {'form': form})

def login(request):
    context = {'title': 'Котокафе Мотя',
               'description': '''LOGIN''',
               'head': 'LOGIN в Кото-кафе "Мотя"!',
               'menu': '''
    <div class="top_menu">
        <a href="/"><div class="selected shadow top_menu_items">Главная</div></a>
        <a href="menu"><div class="shadow top_menu_items">Меню</div></a>
        <a href="contact"><div class="shadow top_menu_items">Контакты</div></a>
    </div>''',
               'center': '''LOGIN''',
               'bottom': '''
    <div id="Reserve">
        <h2>Бронирование</h2>
    </div>'''}
    return render(request, 'index.html', context)



