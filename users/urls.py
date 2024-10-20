from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome),
    path('signup/', views.signup),
    path('login/', views.login),
    path('logout/', views.logout),
]