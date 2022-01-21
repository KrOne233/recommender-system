from cgitb import html
from multiprocessing import context
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Restaurant
from .models import RestaurantSystemUser
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# # Create your views here.
# def welcome_message(request):
#     return HttpResponse ('Welcome')

# #HTML Render 

def welcome_message(request):
    return render(request, 'hello.html')

def show_cover(request):
    return render(request, 'cover.html')

def get_all_ratings(request):
    data = {'rating': RestaurantSystemUser.objects.all()}
    return render(request, 'catalog.html',data)

def get_all_restaurants(request):
    restaurantName =  RestaurantSystemUser.objects.all()
    html = ''
    for r in restaurantName:
        html += f'<h1>{r.reataurant}'
    return render(request, 'catalog.html', restaurantName)
    #return render(request, 'catalog.html',restaurantName)

def get_restaurants(request):
    data = {'reataurant':RestaurantSystemUser.objects.all()}
    return render(request,'catalog.html',data)
    

def user_registration(request):
    if request.user.is_authenticated:
        return redirect('catalog')
    else:
        form = CreateUserForm()
        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account successfully created for' + user)
                return redirect('login')

        context = {'form':form}
        return render(request, 'registration.html',context)

def login_page(request):
    if request.user.is_authenticated:
        return redirect('catalog')
    else:
        if request.method == 'POST':
            username=request.POST.get('username')
            password=request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request,user)
                return redirect('catalog')
            else: 
                messages.info(request, 'Username/Password incorrect')

        context = {}
        return render (request, 'login.html' , context)

def logoutuser(request):
    logout(request)
    return redirect ('login')