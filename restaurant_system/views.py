from cgitb import html
from multiprocessing import context
from django.shortcuts import render, redirect
from django.http import HttpResponse
from numpy import sort
from .models import Restaurant
from .models import RestaurantSystemUser
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
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

@login_required(login_url='login')
def get_restaurants(request):
    restaurants = Restaurant.objects.all()
    return render(request,'catalog.html',{'restaurants':restaurants})
    

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
                model = dump.load("recommender")
                algo = model[0]
                item = pd.read_csv("restaurant.csv")
                prediction = dict()
                for restaurant in item.iloc[:, 0]:
                    pred = algo.predict(username, restaurant, verbose=True)
                    prediction[str(pred[1])] = float(pred[-2])
                sorted(prediction.items())
                return HttpResponse(prediction)

        # return redirect('catalog')
            else: 
                messages.info(request, 'Username/Password incorrect')

        context = {}
        return render (request, 'login.html' , context)

def logoutuser(request):
    logout(request)
    return redirect ('login')
def catalog(request):
    data = {'restaurants': Restaurant.objects.all()}
    return render(request, 'catalog.html',data)


def login_test(request):
    return render(request, 'login_test.html')

def recommendation(request):
    if request.method == "POST":
        user = request.POST.get('username')
        model = dump.load("recommender")
        algo = model[0]
        item = pd.read_csv("restaurant.csv")
        prediction = list()
        for restaurant in item.iloc[:, 0]:
            pred = algo.predict(user, restaurant, verbose=True)
            result = str(pred[1]) + "  " + str(pred[-2])
            prediction.append(result)
        return HttpResponse(prediction)

    return render(request, "login_test.html")
