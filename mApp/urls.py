from django.urls import path, include
from . import views
from .api import RegisterAPI, LoginAPI, UserAPI,FilterAPI,MyPostsAPI,NotificationsAPI
from knox import views as knox_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('api/auth', include('knox.urls')),
    path('api/auth/register', RegisterAPI.as_view(), name='signup'),
    path('api/auth/login', LoginAPI.as_view(), name='login'),
    path('api/auth/user', UserAPI.as_view()),
    path('api/auth/logout', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('users/<int:id>', views.UserProfile.as_view()),
    path('users/<int:id>/change-password', views.ChangePasswordView.as_view(), name='password-update'),
    path('posts', views.AddPostAPI.as_view(), name='add-post'),
    path('posts/<int:id>', views.PostAPI.as_view()),
    path('posts/<int:id>/bids', views.PostBidsAPI.as_view(), name='post-bids'),
    path('bids', views.AddBidAPI.as_view(), name='add-bid'),
    path('bids/<int:id>', views.BidAPI.as_view(), name='bid-api'),
    path('bids/<int:id>/accept', views.AcceptBidAPI.as_view(), name='accept-bid-api'),
    path('api/filter/', FilterAPI.as_view(),name='getitems'),
    path('api/posts/myposts',MyPostsAPI.as_view(),name='myposts'),
    path('api/notifications/getmynotifications',NotificationsAPI.as_view(),name='mynotifs')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
