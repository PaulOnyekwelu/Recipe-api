from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserAPITest(TestCase):
    '''test suite for public user api'''

    def setUp(self):
        self.client = APIClient()
        self.payload = {
            'email': 'test@domain.com',
            'password': 'test123'
        }

    def test_create_valid_user_success(self):
        '''test that users are created successfully with valid data'''

        payload = {**self.payload, 'name': "Test User"}

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn('email', res.data)
        self.assertNotIn('password', res.data)

        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(self.payload['password']))

    def test_user_exist(self):
        '''test user not created if already exists'''
        create_user(**self.payload)
        res = self.client.post(CREATE_USER_URL, self.payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_short(self):
        '''test user not created if password is less than 5 character length'''
        payload = {
            **self.payload,
            'password': 'pw'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(
            email=payload['email']).exists()
        self.assertFalse(user_exists)

    def test_create_token_valid_credential(self):
        '''test that a token is created for valid credentials'''
        create_user(**self.payload)
        res = self.client.post(TOKEN_URL, self.payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('token', res.data)

    def test_create_token_invalid_credential(self):
        '''test that a token is not created for invalid credentials'''
        create_user(**self.payload)
        res = self.client.post(TOKEN_URL,
                               {**self.payload, 'password': 'wrongPass'}
                               )

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        '''test that token is not created if user does not exist'''
        res = self.client.post(TOKEN_URL, self.payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_credential(self):
        '''test that email and password are required fields'''
        res = self.client.post(TOKEN_URL, {'email': '', 'password': ''})

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_me_endpoint_requires_auth(self):
        '''test that user profile is auth-protected'''
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserAPITest(TestCase):
    '''test suite for private user api'''

    def setUp(self):
        self.user = create_user(
            email='test@domain.com',
            password='test123',
            name='Test User'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_profile_success(self):
        '''test that authenticated users access me endpoint'''
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['email'], self.user.email)

    def test_post_me_not_allowed(self):
        '''test that post method is not allowed'''
        res = self.client.post(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        '''test that logged users can update their profile'''
        payload = {'name': 'Updated User', 'password': 'newPass'}
        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
