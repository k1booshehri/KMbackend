from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer, PostSerializer
from .models import Post
from django.db.models import Q
import operator
import functools


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "id": UserSerializer(user, context=self.get_serializer_context()).data.get('id'),
            "token": AuthToken.objects.create(user)[1]
        })


class UserAPI(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class FilterAPI(generics.ListAPIView):

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        queryset = Post.objects.all()
        mypricestart = self.request.GET.get('pricestart', None)
        mypriceend = self.request.GET.get('priceend', None)
        myprovince = self.request.GET.get('province', None)
        mycity = self.request.GET.get('city', None)

        if mypricestart is not None:
            queryset = queryset.filter(price__gt=mypricestart)
        if mypriceend is not None:
            queryset = queryset.filter(price__lt=mypriceend)
        if myprovince is not None:
            queryset = queryset.filter(province=myprovince)
        if mycity is not None:
            queryset = queryset.filter(city=mycity)

        cat = self.request.GET.get('category', None)
        if cat is not None:
            cat = cat.split("$")
            qset = functools.reduce(operator.__or__, [Q(categories__icontains=query) |
                                                      Q(categories__icontains=query) for query in cat])
            queryset = queryset.filter(qset).distinct()
        name = self.request.GET.get('contains', None)
        if name is not None:
            name = name.split()
            qset1 = functools.reduce(operator.__or__, [Q(publisher__icontains=query) |
                                                       Q(title__icontains=query) |
                                                       Q(author__icontains=query) for query in name])

            queryset = queryset.filter(qset1).distinct()

        sort_by = self.request.GET.get('sort', None)
        if sort_by is not None:
            if sort_by == 'price':
                queryset = queryset.order_by('-price').reverse()

        return queryset

class MyPostsAPI(generics.ListAPIView):

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        user=self.request.user
        queryset = Post.objects.all()
        queryset = queryset.filter(owner=user)
        return queryset