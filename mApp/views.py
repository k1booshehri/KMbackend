from rest_framework.response import Response
from rest_framework import status, generics
from rest_condition import And, Or, Not
from .permissions import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from enum import Enum

from mApp.models import User, Post, Categories
from mApp.serializers import UserSerializer, UpdateUserSerializer, AddPostSerializer, PostSerializer


class UserProfile(generics.GenericAPIView):
    permission_classes = [Or(And(IsGetRequest, AllowAny),
                             And(IsPutRequest, IsOwner),
                             And(IsDeleteRequest, IsOwner))]

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


class AddPostAPI(generics.GenericAPIView):
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        if not validate_categories(request.data.get('categories').split('$')):
            return Response({'error': 'Invalid categories'})

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


def validate_categories(categories):
    is_valid = False
    for req_category in categories:
        for category in Categories:
            if str(category).split('.')[1] == req_category:
                is_valid = True
                break

        if is_valid:
            is_valid = False

        else:
            return False

    return True


class PostAPI(generics.GenericAPIView):
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        try:
            post = Post.objects.get(id=kwargs.get('id'))

        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        ser = PostSerializer(post)

        return Response(ser.data, status=status.HTTP_200_OK)


class GetCategories(generics.GenericAPIView):
    def get(self, request, **kwargs):
        new_data = request.data
        counter = 1

        for category in Categories:
            new_data.update({str(category).split('.')[1]: category.value})
            counter += 1

        return Response(new_data, status=status.HTTP_200_OK)
