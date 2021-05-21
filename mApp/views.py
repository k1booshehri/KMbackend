from rest_framework.response import Response
from rest_framework import status, generics
from rest_condition import And, Or, Not
from .permissions import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from enum import Enum
from .models import Notifications

from mApp.models import User, Post, Bid, ChatMessage, ChatThread
from mApp.serializers import UserSerializer, UpdateUserSerializer, AddPostSerializer, PostSerializer, \
    ChangePasswordSerializer, BidSerializer, AddBidSerializer, ChatSerializer


class PostChatAPI(generics.GenericAPIView):
    serializer_class = ChatSerializer
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        try:
            user1 = request.user
            user2 = User.objects.get(id=request.query_params.get('other'))
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        thread = ChatThread.objects.filter(user1=user1.id, user2=user2.id)

        if not len(thread) == 0:
            serializer = ChatSerializer(thread.first())
            ser = UserSerializer(user2)
            return_data = {
                'thread_id': serializer.data.get('id'),
                'user': ser.data,
            }
            return Response(return_data)

        thread = ChatThread.objects.filter(user1=user2.id, user2=user1.id)
        if not len(thread) == 0:
            serializer = ChatSerializer(thread.first())
            ser = UserSerializer(user2)
            return_data = {
                'thread_id': serializer.data.get('id'),
                'user': ser.data,
            }
            return Response(return_data)

        request.data.update({
            'user1': user1.id,
            'user2': user2.id
        })
        serializer = ChatSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        ser = UserSerializer(user2)
        return Response({
                'thread_id': serializer.data.get('id'),
                'user': ser.data
                # 'message': None
        })


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
        new_data = request.data.copy()
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


class AddBidAPI(generics.GenericAPIView):
    serializer_class = AddBidSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        new_data = request.data.copy()
        new_data.update({
            'owner': request.user.id,
        })
        notifowner=Post.objects.get(id=request.data["post"]).owner
        Notifications.objects.create(owner=notifowner,message='New Bid!',post=Post.objects.get(id=request.data["post"]))
        serializer = AddBidSerializer(data=new_data)
        serializer.is_valid(raise_exception=True)
        bid = serializer.save()
        return Response(BidSerializer(bid, context=self.get_serializer_context()).data)


class BidAPI(generics.GenericAPIView):
    permission_classes = [IsBidOwner]

    def delete(self, request, *args, **kwargs):
        try:
            Bid.objects.get(id=kwargs.get('id')).delete()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


class PostBidsAPI(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        try:
            post = Post.objects.get(id=kwargs.get('id'))
            bid = Bid.objects.filter(post=post)

        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        ser = BidSerializer(bid, many=True)

        return Response(ser.data, status=status.HTTP_200_OK)


class AcceptBidAPI(generics.GenericAPIView):
    permission_classes = [IsBidPostOwner]

    def put(self, request, *args, **kwargs):
        serializer = AddBidSerializer(data=request.data)
        bid = Bid.objects.get(id=kwargs.get('id'))

        post = Post.objects.get(id=bid.post.id)
        post.is_active = False
        serializer = AddPostSerializer(data={'post': post})
        serializer.is_valid(raise_exception=True)
        serializer.update(instance=post, validated_data={'post': post})

        request.data.update({'is_accepted': True})
        serializer.is_valid(raise_exception=True)
        updated_bid = serializer.update(instance=bid, validated_data=request.data)
        return Response({
            "bid": BidSerializer(updated_bid, context=self.get_serializer_context()).data
        })
