import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ..models import Post
from ..serializers import PostSerializer


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