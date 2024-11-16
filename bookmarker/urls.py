from django.urls import path
from . import views

app_name = 'bookmarker'

urlpatterns = [
    path('create/', views.image_create, name='create'),
]
