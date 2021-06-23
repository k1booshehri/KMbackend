from rest_framework.response import Response
from rest_framework import status, generics, mixins
from rest_condition import And, Or, Not
from rest_framework.permissions import AllowAny, IsAuthenticated
from enum import Enum

from mApp.models import *
from mApp.serializers import *
from .permissions import *


class GetStoreOrders(generics.GenericAPIView, mixins.ListModelMixin):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        data = Order.objects.filter(post__owner__id=self.request.user.id)
        return data

    def get(self, request, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetUserOrders(generics.GenericAPIView, mixins.ListModelMixin):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        data = Order.objects.filter(user_id=self.request.user)
        return data

    def get(self, request, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderAPI(generics.GenericAPIView):
    serializer_class = OrderSerializer
    permission_classes = [Or(And(IsGetRequest, AllowAny),
                             And(IsPutRequest, IsOrderOwner),
                             And(IsDeleteRequest, IsOrderOwner))]

    def put(self, request, *args, **kwargs):
        try:
            order = Order.objects.get(id=kwargs.get('id'))
            new_address = request.data.get('address')
            order.address = new_address
            order.save()
            return Response({
                "order": OrderSerializer(order, context=self.get_serializer_context()).data
            })
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        Order.objects.get(id=kwargs.get('id')).delete()
        return Response(status=status.HTTP_200_OK)


class AddOrderAPI(generics.GenericAPIView):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        new_data = request.data.copy()
        new_data.update({
            'user': request.user.id
        })

        post = Post.objects.get(id=request.data.get('post'))
        if post.stock == 0:
            return Response({"error": "Not available"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = AddOrderSerializer(data=new_data)
        serializer.is_valid(raise_exception=True)

        post.stock = post.stock - 1
        post.save()

        order = serializer.save()
        return Response({
            "order": OrderSerializer(order, context=self.get_serializer_context()).data
        })


class UserChatsAPI(generics.GenericAPIView):
    serializer_class = ChatSerializer
    return_data = []
    # permission_classes = [And(IsGetRequest, IsChatOwner), ]
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        self.return_data = []

        threads = ChatThread.objects.filter(user1_id=request.user)
        self.chat_info(request, threads)

        threads = ChatThread.objects.filter(user2_id=request.user)
        self.chat_info(request, threads)

        new_data = []
        for i in range(len(self.return_data)):
            if self.return_data[i].get('message').get('thread') is not None:
                new_data.append(self.return_data[i])

        new_data = sorted(new_data, key=lambda x: x['message']['created_at'], reverse=True)
        return Response(new_data, status=status.HTTP_200_OK)

    def chat_info(self, request, threads):
        for i in range(len(threads)):
            if request.user.id == threads[i].user1.id:
                user = User.objects.get(id=threads[i].user2.id)
                self.add_data(threads, user, i)

            else:
                user = User.objects.get(id=threads[i].user1.id)
                self.add_data(threads, user, i)

    def add_data(self, threads, user, i):
        last_message = ChatMessage.objects.filter(thread_id=threads[i].id)

        message_info = ChatMessagesSerializer(last_message.last())
        user_info = UserSerializer(user)
        self.return_data.append({
            'thread_id': threads[i].id,
            'user': user_info.data,
            'message': message_info.data
        })


class MessageAPI(generics.GenericAPIView, mixins.ListModelMixin):
    permission_classes = [Or(And(IsDeleteRequest, IsChatOwner),
                             And(IsPutRequest, IsChatOwner))]

    def delete(self, request, *args, **kwargs):
        try:
            ChatMessage.objects.get(id=kwargs.get('message_id')).delete()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, *args, **kwargs):
        new_data = request.data.copy()
        new_data.update({
            'id': kwargs.get('message_id')
        })
        ser = ChatMessagesSerializer(data=new_data)
        ser.is_valid(raise_exception=True)
        ser.update(instance=ChatMessage.objects.get(id=kwargs.get('message_id')), validated_data=new_data)
        return Response({
            "message": ser.data
        })


class ChatAPI(generics.GenericAPIView, mixins.ListModelMixin):
    serializer_class = ChatMessagesSerializer
    queryset = ChatMessage.objects.all()
    permission_classes = [Or(And(IsGetRequest, IsChatOwner),
                             And(IsPostRequest, IsChatOwner),
                             And(IsPutRequest, IsChatOwner))]

    def get_queryset(self):
        data = ChatMessage.objects.filter(thread_id=self.kwargs.get('thread_id'))
        return data

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        thread_id = self.kwargs.get('thread_id')
        new_data = request.data.copy()
        new_data.update({
            "thread": thread_id,
            "sender": request.user.id
        })
        serializer = ChatMessagesSerializer(data=new_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        try:
            thread = ChatThread.objects.get(id=kwargs.get('thread_id'))
            messages = ChatMessage.objects.filter(thread_id=thread.id)
            if request.user == thread.user1:
                other = thread.user2
            else:
                other = thread.user1

            for message in messages:
                if message.sender == other:
                    data = {
                        'thread_id': thread.id,
                        'is_read': True
                    }
                    ser = ChatMessagesSerializer(data=data)
                    ser.is_valid(raise_exception=True)
                    ser.update(instance=message, validated_data=data)

            return Response(status=status.HTTP_200_OK)

        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
            'owner': request.user
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
