from cgitb import html
from multiprocessing import context

import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse
from numpy import sort

from .models import models, Restaurant, Menu
from .models import Restaurantsystemuser
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm, Rating
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from urllib.parse import urlencode
from surprise import dump
import pandas as pd


# # Create your views here.
# def welcome_message(request):
#     return HttpResponse ('Welcome')

# #HTML Render 

def welcome_message(request):
    return render(request, 'hello.html')


def show_cover(request):
    return render(request, 'cover.html')


# def get_all_ratings(request):   dont need two functionalities
#     data = {'rating': Restaurant.objects.all()}
#     return render(request, 'catalog.html',data)

# remove login required to unrestrict the catalog page
@login_required(login_url='login')
def get_restaurants(request):
    model = dump.load("recommender")
    algo = model[0]
#    item = pd.read_csv("restaurant.csv")
    item = Restaurant.objects.all()
    prediction = dict()
    user = str(request.user)
#    for restaurant in item.iloc[:, 0]:
    for restaurant in item:
        pred = algo.predict(user, restaurant.name, verbose=True)
        prediction[str(pred[1])] = float(pred[-2])
        prediction_ordered = sorted(prediction.items(), key=lambda x: x[1], reverse=True)
    data = list()
    for p in prediction_ordered[0:6]:
        restaurant_name = p[0]
        data.append(item.filter(name=restaurant_name)[0])
    return render(request, 'catalog.html', {'restaurants': data})



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

        context = {'form': form}
        return render(request, 'registration.html', context)


def login_page(request):
    if request.user.is_authenticated:
        return redirect('catalog')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                base_url = reverse('recommendation')
                query_string = urlencode({'user': username})
                url = '{}?{}'.format(base_url, query_string)
                return redirect(url)
            else:
                messages.info(request, 'Username/Password incorrect')
        context = {}
        return render(request, 'login.html', context)


def logoutuser(request):
    logout(request)
    return redirect('login')


def catalog(request):
    if request.GET.get("sort") is not None:
        data = {'restaurants': Restaurant.objects.order_by('co2_score').reverse()}
    else:
        data = {'restaurants': Restaurant.objects.all()}
    return render(request, 'catalog.html', data)


def login_test(request):
    return render(request, 'login_test.html')


def recommendation(request):
    '''
    if request.method == "POST":
        user = request.POST.get('username')

        '''
    model = dump.load("recommender")
    algo = model[0]
    #    item = pd.read_csv("restaurant.csv")
    item = Restaurant.objects.all()
    prediction = dict()
    user = request.GET.get('user')
    #    for restaurant in item.iloc[:, 0]:
    for restaurant in item:
        pred = algo.predict(user, restaurant.name, verbose=True)
        prediction[str(pred[1])] = float(pred[-2])
        prediction_ordered = sorted(prediction.items(), key=lambda x: x[1], reverse=True)
    data = list()
    for p in prediction_ordered[0:6]:
        restaurant_name = p[0]
        data.append(item.filter(name=restaurant_name)[0])
    return render(request, 'catalog.html', {'restaurants': data})


def get_detail(request):
    restaurant_name = request.GET.get('name')
    user = request.GET.get('user')
    menus = Menu.objects.filter(restaurant__iexact=restaurant_name)
    if menus.exists():
        return render(request, 'menu.html', {'menus': menus, 'user': user, 'name': restaurant_name})
    else:
        menu = Menu()
        menu.restaurant = restaurant_name
        menu.menu = "not available"
        menu.description = "not available"
        return render(request, 'menu.html', {'menus': [menu], 'user': user, 'name': restaurant_name})


def rating(request):
    user = request.GET.get('user')
    restaurant_name = request.GET.get('name')
    if request.method == "POST":
        form = Rating(request.POST)
        if form.is_valid():
            rate = request.POST.get('rating')
            Restaurantsystemuser.objects.create(user=user, rating=rate, restaurant=restaurant_name)
            return HttpResponse("Thanks for rating")
        else:
            return HttpResponse("invalid input, please return")
