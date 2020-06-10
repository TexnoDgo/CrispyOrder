# Python
# ----
# Django
from django.shortcuts import render
from django.utils.translation import ugettext as _
# Apps
# ----
# Local
from .models import HomePageFile, CADFile


def index(request):
    model1 = HomePageFile.objects.filter(pk=1)
    model2 = HomePageFile.objects.filter(pk=2)
    model3 = HomePageFile.objects.filter(pk=3)
    context = {
        'model1': model1,
        'model2': model2,
        'model3': model3,
    }

    return render(request, 'HomePage/HomePage.html', context)


def base(request):
    logo = HomePageFile.objects.filter(pk=4)
    context = {
        'logo': logo,
    }
    print(logo)
    return render(request, 'HomePage/base.html', context)


def index2(request):
    return render(request, 'HomePage/example.html')