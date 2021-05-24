import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ..models import Post,User,Bid,Bookmarks
from ..serializers import PostSerializer,UserSerializer,BookMarkSerializer

# initialize the APIClient app
client = Client()


class GetAllPuppiesTest(TestCase):
    """ Test module for GET all Post API """

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


class GetMyPostsTest(TestCase):
    """ Test module for GET all Post API """
    def setUp(self):
        Response=client.post('/api/auth/register',{'username':'abcd@ef.ghi','email':'abcd@ef.ghi','password':'123456'})
        self.sharedvar=Response.json()['token']
        u=User.objects.get(username='abcd@ef.ghi')
        Post.objects.create(owner=u,title='SE modern approach', categories=3, city='tehran')
        Post.objects.create(owner=u,title='Ditel and Ditel', categories=2, city='esfahan')

    def test_get_my_posts(self):
        response = client.get('/api/posts/myposts',HTTP_AUTHORIZATION='token '+self.sharedvar)
        p = Post.objects.all()
        u=User.objects.get(username='abcd@ef.ghi')
        p=p.filter(owner=u)
        serializer = PostSerializer(p, many=True)
        self.assertEqual(response.json()['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)



class BookmarksTest(TestCase):
    def setUp(self):
        Response=client.post('/api/auth/register',{'username':'abcd@ef.ghi','email':'abcd@ef.ghi','password':'123456'})
        self.sharedvar=Response.json()['token']
        u=User.objects.get(username='abcd@ef.ghi')
        Post.objects.create(owner=u,title='SE modern approach', categories=3, city='tehran')

    def setmark(self):
        response1 = client.post('api/bookmarks/setmark',{"markedpost":"1"},HTTP_AUTHORIZATION='token '+self.sharedvar)
        response = client.get('api/bookmarks/getmarks',HTTP_AUTHORIZATION='token '+self.sharedvar)
        b = Bookmarks.objects.all()
        u=User.objects.get(username='abcd@ef.ghi')
        b=p.filter(markedby=u)
        serializer = PostSerializer(p, many=True)
        self.assertEqual(response.json()['results'], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)