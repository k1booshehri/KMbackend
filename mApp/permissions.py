from rest_framework import permissions
from .models import User, Post, Bid


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
