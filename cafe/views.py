from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views import View

from .forms import RegistrationForm, CustomLoginForm
from .models import Product, Category


def index(request):
    main_center_html = get_template("parts/main_center.html").render() # передаем блок из файла для context
    reserve_html = get_template("parts/reserve.html").render()

    context = {'title': 'Котокафе "Мотя"',
               'description': '''
    Здесь можно выпить чаю и уютно провести время в
окружении пушистых друзей. А если вы с кем-то из них
по-настоящему подружились - можете усыновить нового
друга в свою семью''',
               'head': 'Добро пожаловать в Кото-кафе "Мотя"!',
               'center': main_center_html,
               'bottom': reserve_html,
               'main_selected': 'selected',}
    return render(request, 'index.html', context)

def menu(request):
    center_context = products_by_category() # можно передавать в контекст и в parts
    menu_center_html = get_template("parts/menu_center.html").render(center_context)

    context = {'title': 'Котокафе "Мотя"',
               'description': '''У нас много разных вкусняшек для вас и ваших питомцев''',
               'head': 'Меню от "Моти"',
               'center': menu_center_html,
               'menu_selected': 'selected',}
    return render(request, 'index.html', context)


def contact(request):
    center_context = {'bake': "----Выпечка-----"} # можно передавать в контекст и в parts
    context_center_html = get_template("parts/contact_center.html").render(center_context)

    context = {'title': 'Контакты "Моти"',
               'contact_selected': 'selected',
               'description': '''Ждем вас в гости''',
               'head': 'Контакты "Моти"',
               'center': context_center_html,
               }
    return render(request, 'index.html', context)

###############################################################################

def products_by_category():
    """Вывод продуктов по категориям"""
    categories = Category.objects.prefetch_related('products').all()
    products = Product.objects.select_related('category').all()
    context = {
        'categories': categories,
        'products': products
    }
    return context# ////////////////////////////////////////////////////

class RegistrationView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            user = form.save()
            messages.success(request, f'Регистрация успешно завершена! Добро пожаловать, {user.first_name}!')
            return redirect('login')  # Перенаправление на страницу входа   login
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{form.fields[field].label}: {error}')
        return render(request, 'register.html', {'form': form})


class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = 'login.html'
    success_url = reverse_lazy('index')  # Перенаправление после успешного входа
    redirect_authenticated_user = True  # Перенаправлять уже авторизованных пользователей

    def get_success_url(self):
        # Можно добавить логику для перенаправления на разные страницы
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return self.success_url

    def form_valid(self, form):
        # при успешной авторизации
        response = super().form_valid(form)
        return response

    def form_invalid(self, form):
        # при неудачной авторизации
        return super().form_invalid(form)


class CustomLogoutView:
    @staticmethod
    def logout_view(request):
        print(f'User: "{request.user}" logged out.')
        logout(request)
        return redirect('login')