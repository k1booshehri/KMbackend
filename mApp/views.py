from rest_framework.response import Response
from rest_framework import status, generics
from rest_condition import And, Or, Not
from .permissions import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from enum import Enum

from mApp.models import User, Post
from mApp.serializers import UserSerializer, UpdateUserSerializer, AddPostSerializer, PostSerializer, \
    ChangePasswordSerializer


class UserProfile(generics.GenericAPIView):
    permission_classes = [Or(And(IsGetRequest, AllowAny),
                             And(IsPutRequest, IsAccountOwner),
                             And(IsDeleteRequest, IsAccountOwner))]

    def get(self, request, **kwargs):
        try:
            user = User.objects.get(id=kwargs.get('id'))

        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        ser = UserSerializer(user)

        return Response(ser.data, status=status.HTTP_200_OK)

    def put(self, request, **kwargs):
        try:
            user = User.objects.get(id=kwargs.get('id'))
            request.data.update({'id': kwargs.get('id')})
            request.data.update({'username': user.username})
            ser = UpdateUserSerializer(user, data=request.data)
            if ser.is_valid():
                ser.update(instance=user, validated_data=request.data)
                return Response(ser.data, status=status.HTTP_200_OK)

            else:
                return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, **kwargs):
        try:
            User.objects.get(id=kwargs.get('id')).delete()
            return Response(status=status.HTTP_200_OK)

        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated, IsAccountOwner)

    def get_object(self, queryset=None):
        self.request.data.update({'id': self.kwargs.get('id')})
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddPostAPI(generics.GenericAPIView):
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        new_data = request.data
        new_data.update({
            'owner': request.user,
        })
        serializer = AddPostSerializer(data=new_data)
        serializer.is_valid(raise_exception=True)
        post = serializer.save()
        return Response({
            "post": PostSerializer(post, context=self.get_serializer_context()).data
        })


class PostAPI(generics.GenericAPIView):
    serializer_class = PostSerializer
    permission_classes = [Or(And(IsGetRequest, AllowAny),
                             And(IsPutRequest, IsPostOwner),
                             And(IsDeleteRequest, IsPostOwner))]

    def get(self, request, *args, **kwargs):
        try:
            post = Post.objects.get(id=kwargs.get('id'))

        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        ser = PostSerializer(post)

        return Response(ser.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        serializer = AddPostSerializer(data=request.data)
        post = Post.objects.get(id=kwargs.get('id'))
        request.data.update({'owner': User.objects.get(id=post.owner.id)})
        serializer.is_valid(raise_exception=True)
        updated_post = serializer.update(instance=post, validated_data=request.data)
        return Response({
            "event": PostSerializer(updated_post, context=self.get_serializer_context()).data
        })

    def delete(self, request, *args, **kwargs):
        Post.objects.get(id=kwargs.get('id')).delete()
        return Response(status=status.HTTP_200_OK)
