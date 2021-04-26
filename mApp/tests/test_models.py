from django.test import TestCase
from ..models import Post


class PostTest(TestCase):
    """ Test module for Post model """

    def setUp(self):
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