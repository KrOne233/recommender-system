from django.shortcuts import render
from django.http import HttpResponse
from .models import Restaurant
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