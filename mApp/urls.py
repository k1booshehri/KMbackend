from django.urls import path, include
from . import views
from .api import RegisterAPI, LoginAPI, UserAPI
from knox import views as knox_views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('api/auth', include('knox.urls')),
    path('api/auth/register', RegisterAPI.as_view()),
    path('api/auth/login', LoginAPI.as_view()),
    path('api/auth/user', UserAPI.as_view()),
    path('api/auth/logout', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('users/<int:id>', views.UserProfile.as_view()),
    path('posts', views.AddPostAPI.as_view()),
]
