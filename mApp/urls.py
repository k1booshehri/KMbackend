from django.urls import path, include
from . import views
from .api import RegisterAPI, LoginAPI, UserAPI,FilterAPI,MyPostsAPI,NotificationsAPI,MakeBookMarkAPI,GetMarksAPI,BidUpdateAPI,IsMarkedAPI,DeMarkAPI
from knox import views as knox_views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('api/auth', include('knox.urls')),
    path('api/auth/register', RegisterAPI.as_view(), name='signup'),
    path('api/auth/login', LoginAPI.as_view(), name='login'),
    path('api/auth/user', UserAPI.as_view()),
    path('api/auth/logout', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('api/users/<int:id>', views.UserProfile.as_view()),
    path('api/users/<int:id>/change-password', views.ChangePasswordView.as_view(), name='password-update'),
    path('api/users/chats', views.UserChatsAPI.as_view()),
    path('api/posts', views.AddPostAPI.as_view(), name='add-post'),
    path('api/posts/<int:id>', views.PostAPI.as_view()),
    path('api/posts/<int:id>/bids', views.PostBidsAPI.as_view(), name='post-bids'),
    path('api/bids', views.AddBidAPI.as_view(), name='add-bid'),
    path('api/bids/<int:id>', views.BidAPI.as_view(), name='bid-api'),
    path('api/bids/<int:id>/accept', views.AcceptBidAPI.as_view(), name='accept-bid-api'),
    path('api/filter/', FilterAPI.as_view(),name='getitems'),
    path('api/posts/myposts',MyPostsAPI.as_view(),name='myposts'),
    path('api/notifications/getmynotifications',NotificationsAPI.as_view(),name='mynotifs'),
    path('api/bookmarks/setmark', MakeBookMarkAPI.as_view(), name='setmark'),
    path('api/bookmarks/getmarks', GetMarksAPI.as_view(), name='getmarks'),
    path('api/bids/edit', BidUpdateAPI.as_view(), name='editbid'),
    path('api/bookmarks/ismarked', IsMarkedAPI.as_view(), name='ismarked'),
    path('api/chat', views.PostChatAPI.as_view()),
    path('api/chat/<int:thread_id>', views.ChatAPI.as_view()),
    path('api/message', views.ChatAPI.as_view()),
    path('api/message/<int:message_id>', views.MessageAPI.as_view()),
    path('api/bookmarks/demark', DeMarkAPI.as_view(), name='demark')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
