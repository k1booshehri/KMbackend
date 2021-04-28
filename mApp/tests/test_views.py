import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ..models import User, Post, Bid
from ..serializers import PostSerializer

# initialize the APIClient app
client = Client()


class GetAllPuppiesTest(TestCase):
    """ Test module for GET all Post API """

    def setUp(self):
        client = Client()
        self.add_bid_url = reverse('add-bid')
        self.bid_url = reverse('bid-api', args='1')
        self.post_bids_url = reverse('post-bids', args='1')

        User.objects.create(username='masih@gmail.com',
                            email='masih@gmail.com',
                            first_name='masih',
                            last_name='bn',
                            password='123456',
                            phone_number=9125557558,
                            university='iust',
                            field_of_study='ce',
                            entry_year=97)

        Post.objects.create(owner=User.objects.get(id=1),
                            title='riazi 1 faramarzi',
                            author='faramarzi',
                            publisher='gaj',
                            categories='math$riazi',
                            price=10000,
                            province='tehran',
                            zone='narmak',
                            status='sell',
                            description='some description',
                            is_active=True)

        Bid.objects.create(post=Post.objects.get(id=1),
                           owner=User.objects.get(id=1),
                           offered_price=9000,
                           description='some random description')

        Bid.objects.create(post=Post.objects.get(id=1),
                           owner=User.objects.get(id=1),
                           offered_price=19000,
                           description='some other random description')

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

    def test_post_bids_GET(self):
        response = self.client.get(self.post_bids_url)

        self.assertEqual(response.status_code, 200)
