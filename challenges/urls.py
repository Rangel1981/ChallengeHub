from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('challenges/', views.challenge_list, name='challenge_list'),
    path('create/', views.challenge_create, name='challenge_create'),
    path('<int:challenge_id>/', views.challenge_detail, name='challenge_detail'),
    
    # Rotas de Autenticação
    path('register/', views.register_view, name='register'),
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
