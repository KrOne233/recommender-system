from django.urls import path
from.import views
urlpatterns = [
    path('homepage/', views.welcome_message),
    path('cover/', views.show_cover), #show_cover = name of function, cover is url
    path('catalog/', views.catalog),
    path('login_test/', views.login_test),
    path('index/', views.recommendation),
]

