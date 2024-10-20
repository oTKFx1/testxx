from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome),
    path('create_consultant/', views.initiate_consultation),
    path('fetch_consultant/', views.fetch_consultants),
    path('send_message/', views.send_message),
    path('fetch_messages/', views.fetch_messages),
    path('complete_consultant/', views.complete_consultant),
    path('review_specialist/', views.review_specialist),
    path('report_consultant/', views.report_consultant),
]
