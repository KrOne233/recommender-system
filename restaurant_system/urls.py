from django.urls import path
from.import views
urlpatterns = [
    path('homepage/', views.welcome_message),
    path('cover/', views.show_cover), #show_cover = name of function, cover is url
    path('catalog/', views.catalog),
    path('login/', views.login_page),
    path('registration/', views.user_registration)
    
]

