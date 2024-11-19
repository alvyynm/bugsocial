from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from . import views

urlpatterns = [
    # path('login/', views.user_login, name='login'),
    path('', include('django.contrib.auth.urls')),
    path('dashboard/', views.dashboards, name='dashboard'),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('users/', views.user_list, name='user_list'),
    path('users/follow', views.user_follow, name='user_follow'),
    path('users/<username>/', views.user_detail, name='user_detail'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
