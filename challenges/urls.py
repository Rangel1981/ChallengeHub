from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('challenges/', views.challenge_list, name='challenge_list'),
    path('create/', views.create_challenge, name='challenge_create'),
    path('<int:challenge_id>/', views.challenge_detail, name='challenge_detail'),
]
