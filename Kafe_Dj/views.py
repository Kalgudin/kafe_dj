from django.shortcuts import render


def index(request):
    context = {'title': 'Котокафе Мотя', 'description': 'Some Description'}
    return render(request, 'index.html', context)



def menu(request):
    context = {'title': 'Котокафе Мотя', 'description': 'Some Description'}
    return render(request, 'menu.html', context)


def contact(request):
    context = {'title': 'Котокафе Мотя', 'description': 'Some Description'}
    return render(request, 'contact.html', context)


