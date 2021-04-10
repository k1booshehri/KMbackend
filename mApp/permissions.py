from rest_framework import permissions
from .models import User


class IsOwner(permissions.BasePermission):
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
