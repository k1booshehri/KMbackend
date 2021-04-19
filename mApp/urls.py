from django.urls import path, include
from . import views
from .api import RegisterAPI, LoginAPI, UserAPI,FilterAPI
from knox import views as knox_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('api/auth', include('knox.urls')),
    path('api/auth/register', RegisterAPI.as_view()),
    path('api/auth/login', LoginAPI.as_view()),
    path('api/auth/user', UserAPI.as_view()),
    path('api/auth/logout', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('users/<int:id>', views.UserProfile.as_view()),
    path('users/<int:id>/change-password', views.ChangePasswordView.as_view(), name='password-update'),
    path('posts', views.AddPostAPI.as_view()),
    path('posts/<int:id>', views.PostAPI.as_view()),
    path('api/filter/', FilterAPI.as_view(),name='getitems'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
