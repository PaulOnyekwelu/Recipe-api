from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag
from recipe.serializers import TagSerializer


TAG_LIST_URL = reverse('recipe:tags-list')


def create_sample_user(email='test@domain.com', password='testPass'):
    '''create and return a test user'''
    return get_user_model().objects.create_user(email, password)


class PublicTagTest(TestCase):
    '''test suite for tag public api'''

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        '''tests that the tag api endpoint is auth-protected'''
        res = self.client.get(TAG_LIST_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagTest(TestCase):
    '''test suite for tag private api'''

    def setUp(self):
        self.client = APIClient()
        self.user = create_sample_user()
        self.client.force_authenticate(self.user)

    def test_tag_listing(self):
        '''test that tag list api is successful'''
        Tag.objects.create(name='Drinks', user=self.user)
        Tag.objects.create(name='Pie', user=self.user)

        res = self.client.get(TAG_LIST_URL)

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_listing_limited_to_auth_user(self):
        '''test that return tags belong to authenticated user'''
        user2 = create_sample_user('other@domain.com', 'test222')
        Tag.objects.create(user=user2, name='Flaky')
        tag = Tag.objects.create(user=self.user, name='Vegan')

        res = self.client.get(TAG_LIST_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)

    def test_create_tag_success(self):
        '''test that tags are created successfully'''
        payload = {'name': 'Testy'}
        self.client.post(TAG_LIST_URL, payload)

        exist = Tag.objects.filter(
            user=self.user, name=payload['name']).exists()

        self.assertTrue(exist)

    def test_create_tag_invalid(self):
        '''test create tag with invalid payload'''
        res = self.client.post(TAG_LIST_URL, {'name': ''})

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
