from unicodedata import name
from django.urls import path
from.import views
urlpatterns = [
    # path('homepage/', views.welcome_message),
    # path('cover/', views.show_cover), #show_cover = name of function, cover is url
    path('catalog/', views.get_restaurants, name ="catalog"),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logoutuser, name='logout'),
    path('registration/', views.user_registration, name="registration"), 
    path('catalog2/', views.catalog),
    path('login_test/', views.login_test),
    path('index/', views.recommendation, name='recommendation'),
    path('detail/', views.get_detail, name='detail'),
    path('rating/', views.rating, name='rating'),
]

