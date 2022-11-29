from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserAPITest(TestCase):
    '''test suite for user api'''

    def setUp(self):
        self.client = APIClient()
        self.payload = {
            'email': 'test@domain.com',
            'password': 'test123',
            'name': 'Test User'
        }

    def test_create_valid_user_success(self):
        '''test that users are created successfully with valid data'''

        res = self.client.post(CREATE_USER_URL, data=self.payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn('email', res.data)
        self.assertNotIn('password', res.data)

        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(self.payload['password']))

    def test_user_exist(self):
        '''test user not created if already exists'''
        create_user(**self.payload)
        res = self.client.post(CREATE_USER_URL, data=self.payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_short(self):
        '''test user not created if password is less than 5 character length'''
        payload = {
            **self.payload,
            'password': 'pw'
        }
        res = self.client.post(CREATE_USER_URL, data=payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(
            email=payload['email']).exists()
        self.assertFalse(user_exists)
