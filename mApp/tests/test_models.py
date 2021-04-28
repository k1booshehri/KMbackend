from django.test import TestCase
from ..models import User, Post, Bid


class TestModels(TestCase):
    """ Test module for Post model """

    def setUp(self):
        User.objects.create(username='masih@gmail.com',
                            email='masih@gmail.com',
                            first_name='masih',
                            last_name='bn',
                            password='123456',
                            phone_number=9125557558,
                            university='iust',
                            field_of_study='ce',
                            entry_year=97)

        User.objects.create(username='kayvan@gmail.com',
                            email='kayvan@gmail.com',
                            first_name='kayvan',
                            last_name='bs',
                            password='123456',
                            phone_number=9126667558,
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

        Post.objects.create(owner=User.objects.get(id=1),
                            title='riazi 2 faramarzi',
                            author='faramarzi',
                            publisher='gaj',
                            categories='math$riazi',
                            price=23000,
                            province='tehran',
                            zone='narmak',
                            status='sell',
                            description='some description',
                            is_active=True)

        Post.objects.create(
            title='SE modern approach', categories=3, city='tehran')
        Post.objects.create(
            title='Ditel and Ditel', categories=2, city='esfahan')

    def test_get_city(self):
        p1 = Post.objects.get(title='SE modern approach')
        p2 = Post.objects.get(title='Ditel and Ditel')
        self.assertEqual(
            p1.get_city(), "SE modern approach is in tehran city.")
        self.assertEqual(
            p2.get_city(), "Ditel and Ditel is in esfahan city.")

    def test_bid_owner_and_post(self):
        b1 = Bid.objects.create(post=Post.objects.get(id=1),
                                owner=User.objects.get(id=2),
                                offered_price=9000,
                                description='some random description')

        self.assertEqual(b1.owner, User.objects.get(id=2))
        self.assertEqual(b1.post, Post.objects.get(id=1))
