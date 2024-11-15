from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    # path('login/', views.user_login, name='login'),
    path('login/', auth_views.LoginView(), name='login'),
    path('logout/', auth_views.LogoutView(), name='logout'),
    path('dashboard/', views.dashboards, name='dashboard')
]
