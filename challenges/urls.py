from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('challenges/', views.challenge_list, name='challenge_list'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create/', views.challenge_create, name='challenge_create'),
    path('<int:challenge_id>/', views.challenge_detail, name='challenge_detail'),
    path('checkin/<int:challenge_id>/', views.checkin_challenge, name='checkin_challenge'),
    path('<int:challenge_id>/checkin/', views.checkin_challenge, name='checkin_challenge'),
    path('feed/', views.feed, name='feed'),
    path('<int:challenge_id>/comment/', views.add_comment, name='add_comment'),
    path('notifications/read/', views.mark_notifications_read, name='mark_notifications_read'),

    # Rotas de Autenticação
    path('register/', views.register_view, name='register'),
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
