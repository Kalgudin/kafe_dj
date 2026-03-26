from django.shortcuts import render


def main(request):
    context = {'title': 'main',
               'description': 'main description',
               'head': 'IN Management',

               }
    return render(request, 'management.html', context)

