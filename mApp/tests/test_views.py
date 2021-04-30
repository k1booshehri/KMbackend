import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ..models import Post,User
from ..serializers import PostSerializer,UserSerializer


# initialize the APIClient app
client = Client()


class GetAllPuppiesTest(TestCase):
    """ Test module for GET all Post API """

    def setUp(self):
        Post.objects.create(title='SE modern approach', categories=3, city='tehran')
        Post.objects.create(title='Ditel and Ditel', categories=2, city='esfahan')

    def test_get_all_puppies(self):
        # get API response
        response = client.get(reverse('getitems'))
        # get data from db
        p = Post.objects.all()
        serializer = PostSerializer(p, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

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
        self.assertEqual(response.json(), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)