from django.shortcuts import render
from django.http import HttpResponse
from .models import Restaurant

# # Create your views here.
# def welcome_message(request):
#     return HttpResponse ('Welcome')

# #HTML Render 

def welcome_message(request):
    return render(request, 'hello.html')

def show_cover(request):
    return render(request, 'cover.html')

def catalog(request):
    data = {'restaurants': Restaurant.objects.all()}
    return render(request, 'catalog.html',data)

def login_page(request):
    return render(request, 'login.html')