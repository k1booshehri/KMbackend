from rest_framework import permissions
from .models import User, Post, Bid, ChatThread, ChatMessage, Order


class IsOrderOwner(permissions.BasePermission):
    def has_permission(self, request, view, **kwargs):
        try:
            order = Order.objects.get(id=view.kwargs.get('id'))
        except e:
            return False

        if not request.user.username == order.user.username:
            return False

        else:
            return True


class IsChatOwner(permissions.BasePermission):
    def has_permission(self, request, view, **kwargs):
        try:
            chat = ChatThread.objects.get(id=view.kwargs.get('thread_id'))
        except:
            return self.check_message(request, view)

        if request.user.id == chat.user1.id:
            return True

        if request.user.id == chat.user2.id:
            return True

        return False

    def check_message(self, request, view):
        try:
            thread_id = ChatMessage.objects.get(id=view.kwargs.get('message_id')).thread.id
            chat = ChatThread.objects.get(id=thread_id)
        except:
            return self.check_thread(request)

        if request.user.id == chat.user1.id:
            return True

        if request.user.id == chat.user2.id:
            return True

        return False

    def check_thread(self, request):
        try:
            chat = ChatThread.objects.get(id=request.data.get('thread'))
        except:
            return False

        if request.user.id == chat.user1.id:
            return True

        if request.user.id == chat.user2.id:
            return True

        return False


class IsBidPostOwner(permissions.BasePermission):
    def has_permission(self, request, view, **kwargs):
        try:
            bid = Bid.objects.get(id=view.kwargs.get('id'))
        except:
            return False

        if not request.user.username == bid.post.owner.username:
            return False

        else:
            return True


class IsBidOwner(permissions.BasePermission):
    def has_permission(self, request, view, **kwargs):
        try:
            bid = Bid.objects.get(id=view.kwargs.get('id'))
        except:
            return False

        if not request.user.username == bid.owner.username:
            return False

        else:
            return True


class IsPostOwner(permissions.BasePermission):
    def has_permission(self, request, view, **kwargs):
        try:
            post = Post.objects.get(id=view.kwargs.get('id'))
        except:
            return False

        if not request.user.username == post.owner.username:
            return False

        else:
            return True


class IsAccountOwner(permissions.BasePermission):
    def has_permission(self, request, view, **kwargs):
        try:
            user = User.objects.get(id=view.kwargs.get('id'))
        except:
            return False

        if not request.user.username == user.username:
            return False

        else:
            return True


class IsPostRequest(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method == "POST"


class IsPutRequest(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method == "PUT"


class IsGetRequest(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method == "GET"


class IsDeleteRequest(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method == "DELETE"
