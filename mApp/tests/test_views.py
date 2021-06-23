import json
from rest_framework import status
from django.test import TestCase, Client
from rest_framework.test import APIClient
from django.urls import reverse
from ..models import Post, User, Bid
from ..serializers import PostSerializer, UserSerializer, ChatSerializer

client = Client()


class GetAllPuppiesTest(TestCase):

    def setUp(self):
        client = Client()
        self.login_url = reverse('login')
        self.signup_url = reverse('signup')
        self.add_post_url = reverse('add-post')
        self.add_bid_url = reverse('add-bid')
        self.bid_url = reverse('bid-api', args='1')
        self.accept_bid_url = reverse('accept-bid-api', args='1')
        self.post_bids_url = reverse('post-bids', args='1')

        client.post(self.signup_url, {
            "username": "mrBn@gmail.com",
            "email": "mrBn@gmail.com",
            "first_name": "masih",
            "last_name": "bahmani",
            "password": "123456",
            "phone_number": "56662148951",
            "university": "iust",
            "field_of_study": "CE",
            "entry_year": "97"
        })

        client.post(self.signup_url, {
            "username": "k1@gmail.com",
            "email": "k1@gmail.com",
            "first_name": "k1",
            "last_name": "bs",
            "password": "123456",
            "phone_number": "5356662148951",
            "university": "iust",
            "field_of_study": "CE",
            "entry_year": "97"
        })

        client.post(self.signup_url, {
            "username": "matin@gmail.com",
            "email": "matin@gmail.com",
            "first_name": "matin",
            "last_name": "mrjn",
            "password": "123456",
            "phone_number": "5344662148951",
            "university": "iust",
            "field_of_study": "CE",
            "entry_year": "97"
        })

        respomse = client.post(self.signup_url, {
            "username": "masih@gmail.com",
            "email": "masih@gmail.com",
            "first_name": "masih",
            "last_name": "bnn",
            "password": "123456",
            "phone_number": "534468951",
            "is_store": True,
            "store_name": "Book City"
        })

        Post.objects.create(owner=User.objects.get(id=1),
                            title='riazi 1 faramarzi',
                            author='faramarzi',
                            publisher='gaj',
                            categories='math$riazi',
                            price="10000",
                            province='tehran',
                            zone='narmak',
                            status='sell',
                            description='some description',
                            is_active="True")

        Post.objects.create(owner=User.objects.get(id=4),
                            title='riazi 2 faramarzi',
                            author='faramarzi',
                            publisher='gaj',
                            categories='math$riazi',
                            price="10000",
                            status='sell',
                            description='some description',
                            is_active="True",
                            stock=10,
                            is_from_store=True)

        Bid.objects.create(post=Post.objects.get(id=1),
                           owner=User.objects.get(id=2),
                           offered_price="9000",
                           description='some random description')

        Bid.objects.create(post=Post.objects.get(id=1),
                           owner=User.objects.get(id=1),
                           offered_price="19000",
                           description='some other random description')

        Post.objects.create(title='SE modern approach', categories=3, city='tehran')
        Post.objects.create(title='Ditel and Ditel', categories=2, city='esfahan')

    def test_get_all_puppies(self):
        # get API response
        response = client.get(reverse('getitems'))
        # get data from db
        p = Post.objects.all()
        serializer = PostSerializer(p, many=True)
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_bids_GET(self):
        response = self.client.get(self.post_bids_url)

        self.assertEqual(response.status_code, 200)

    def test_add_bids_POST(self):
        login_bid_owner = self.client.post(self.login_url, {
            "username": "k1@gmail.com",
            "password": "123456",
        })
        response = self.client.post(self.add_bid_url, {
                "post": 1,
                "offered_price": 10000,
                "description": "wanna buy this"
        },
            HTTP_AUTHORIZATION='token ' + login_bid_owner.json()['token'])

        self.assertEqual(response.status_code, 200)

    def test_bids_DELETE(self):
        login_bid_owner = self.client.post(self.login_url, {
            "username": "k1@gmail.com",
            "password": "123456",
        })

        response = self.client.delete(self.bid_url, HTTP_AUTHORIZATION='token ' + login_bid_owner.json()['token'])

        self.assertEqual(response.status_code, 200)

    def test_accept_bids(self):
        login_post_owner = self.client.post(self.login_url, {
            "username": "mrBn@gmail.com",
            "password": "123456",
        })

        response = self.client.put(self.accept_bid_url, HTTP_AUTHORIZATION='token ' + login_post_owner.json()['token'])

        self.assertEqual(response.status_code, 200)

    def test_get_chat_thread_id(self):
        login_post_owner = self.client.post(self.login_url, {
            "username": "mrBn@gmail.com",
            "password": "123456",
        })

        other_user = 2
        response = self.client.get(
            '/api/chat?other=' + str(other_user),
            HTTP_AUTHORIZATION='token ' + login_post_owner.json()['token']
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['user']['id'], other_user)

    def test_chat_send_message(self):
        login_post_owner = self.client.post(self.login_url, {
            "username": "mrBn@gmail.com",
            "password": "123456",
        })

        other_user = 2
        get_chat_response = self.client.get(
            '/api/chat?other=' + str(other_user),
            HTTP_AUTHORIZATION='token ' + login_post_owner.json()['token']
        )

        message_content = 'Hi, you good?'
        response = self.client.post(
            '/api/chat/' + str(get_chat_response.json()['thread_id']),
            {'message': message_content},
            HTTP_AUTHORIZATION='token ' + login_post_owner.json()['token'],
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], message_content)
        self.assertEqual(response.json()['reply_of'], None)
        self.assertEqual(response.json()['thread'], get_chat_response.json()['thread_id'])
        self.assertEqual(response.json()['sender'], 1)

    def test_chat_get_messages(self):
        login_user1 = self.client.post(self.login_url, {
            "username": "mrBn@gmail.com",
            "password": "123456",
        })

        other_user = 2
        get_chat_response = self.client.get(
            '/api/chat?other=' + str(other_user),
            HTTP_AUTHORIZATION='token ' + login_user1.json()['token']
        )

        message_content = 'Hi'
        self.client.post(
            '/api/chat/' + str(get_chat_response.json()['thread_id']),
            {'message': message_content},
            HTTP_AUTHORIZATION='token ' + login_user1.json()['token'],
        )
        message_content = 'you good?'
        self.client.post(
            '/api/chat/' + str(get_chat_response.json()['thread_id']),
            {'message': message_content},
            HTTP_AUTHORIZATION='token ' + login_user1.json()['token'],
        )
        message_content = 'you good?'
        self.client.post(
            '/api/chat/' + str(get_chat_response.json()['thread_id']),
            {'message': message_content},
            HTTP_AUTHORIZATION='token ' + login_user1.json()['token'],
        )

        response = self.client.get(
            '/api/chat/' + str(get_chat_response.json()['thread_id']),
            HTTP_AUTHORIZATION='token ' + login_user1.json()['token']
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(type(response.json()), list)

    def test_chat_send_is_read(self):
        login_post_owner = self.client.post(self.login_url, {
            "username": "mrBn@gmail.com",
            "password": "123456",
        })

        other_user = 2
        get_chat_response = self.client.get(
            '/api/chat?other=' + str(other_user),
            HTTP_AUTHORIZATION='token ' + login_post_owner.json()['token']
        )

        message_content = 'Hi, you good?'
        self.client.post(
            '/api/chat/' + str(get_chat_response.json()['thread_id']),
            {'message': message_content},
            HTTP_AUTHORIZATION='token ' + login_post_owner.json()['token'],
        )

        response = self.client.put(
            '/api/chat/' + str(get_chat_response.json()['thread_id']),
            HTTP_AUTHORIZATION='token ' + login_post_owner.json()['token'],
        )

        self.assertEqual(response.status_code, 200)

    def test_chat_delete_message(self):
        login_post_owner = self.client.post(self.login_url, {
            "username": "mrBn@gmail.com",
            "password": "123456",
        })

        other_user = 2
        get_chat_response = self.client.get(
            '/api/chat?other=' + str(other_user),
            HTTP_AUTHORIZATION='token ' + login_post_owner.json()['token']
        )

        message_content = 'Hi, you good?'
        send_msg_response = self.client.post(
            '/api/chat/' + str(get_chat_response.json()['thread_id']),
            {'message': message_content},
            HTTP_AUTHORIZATION='token ' + login_post_owner.json()['token'],
        )

        response = self.client.delete(
            '/api/message/' + str(send_msg_response.json()['id']),
            HTTP_AUTHORIZATION='token ' + login_post_owner.json()['token'],
        )

        self.assertEqual(response.status_code, 200)

    def test_chat_edit_message(self):
        login_post_owner = self.client.post(self.login_url, {
            "username": "mrBn@gmail.com",
            "password": "123456",
        })

        other_user = 2
        get_chat_response = self.client.get(
            '/api/chat?other=' + str(other_user),
            HTTP_AUTHORIZATION='token ' + login_post_owner.json()['token']
        )

        message_content = 'Hi, you good?'
        send_msg_response = self.client.post(
            '/api/chat/' + str(get_chat_response.json()['thread_id']),
            {'message': message_content},
            HTTP_AUTHORIZATION='token ' + login_post_owner.json()['token'],
        )

        new_message_content = 'the new message'
        response = APIClient().put(
            '/api/message/' + str(send_msg_response.json()['id']),
            {'message': new_message_content},
            HTTP_AUTHORIZATION='token ' + login_post_owner.json()['token'],
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message']['message'], new_message_content)

    def test_chat_get_chats(self):
        login_post_owner = self.client.post(self.login_url, {
            "username": "mrBn@gmail.com",
            "password": "123456",
        })

        other_user = 2
        self.client.get(
            '/api/chat?other=' + str(other_user),
            HTTP_AUTHORIZATION='token ' + login_post_owner.json()['token']
        )

        other_user = 3
        self.client.get(
            '/api/chat?other=' + str(other_user),
            HTTP_AUTHORIZATION='token ' + login_post_owner.json()['token']
        )

        response = self.client.get(
            '/api/users/chats',
            HTTP_AUTHORIZATION='token ' + login_post_owner.json()['token'],
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.json()), list)

    def test_post_order(self):
        login_owner = self.client.post(self.login_url, {
            "username": "matin@gmail.com",
            "password": "123456",
        })

        post_id = 2
        response = self.client.post(
            '/api/order',
            HTTP_AUTHORIZATION='token ' + login_owner.json()['token'],
            data={
                "post": post_id,
                "address": "this st, that st, the other st"
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['order']['user']['id'], login_owner.data['id'])
        self.assertEqual(response.data['order']['post']['id'], post_id)


class GetMyPostsTest(TestCase):
    def setUp(self):
        Response=client.post('/api/auth/register',{'username':'abcd@ef.ghi','email':'abcd@ef.ghi','password':'123456'})
        self.sharedvar=Response.json()['token']
        u=User.objects.get(username='abcd@ef.ghi')
        Post.objects.create(owner=u,title='SE modern approach', categories=3, city='tehran')
        Post.objects.create(owner=u,title='Ditel and Ditel', categories=2, city='esfahan')

    def test_get_my_posts(self):
        response = client.get('/api/posts/myposts', HTTP_AUTHORIZATION='token '+self.sharedvar)
        p = Post.objects.all()
        u=User.objects.get(username='abcd@ef.ghi')
        p=p.filter(owner=u)
        serializer = PostSerializer(p, many=True)
        self.assertEqual(response.json()['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
