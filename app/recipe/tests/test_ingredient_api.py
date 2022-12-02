from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient
from recipe.serializers import IngredientSerializer

INGREDIENT_LIST_URL = reverse('recipe:ingredient-list')


def create_sample_user(email='test@domain.com', password='testPass'):
    '''create and return a test user'''
    return get_user_model().objects.create_user(email, password)


def create_ingredient(user=None, name="test ingredient"):
    '''create and return a test ingredient'''
    return Ingredient.objects.create(user=user, name=name)


class PublicIngredientAPITest(TestCase):
    '''test suites for public access to ingredient api'''

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        '''test that ingredient api endpoint is auth-protected'''
        res = self.client.get(INGREDIENT_LIST_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientAPITest(TestCase):
    '''test suite for private access to ingredient api'''

    def setUp(self):
        self.client = APIClient()
        self.user = create_sample_user()
        self.client.force_authenticate(self.user)

    def test_ingredient_listing(self):
        '''test that ingredient listing api is successful'''
        create_ingredient(self.user, 'Gauva')
        create_ingredient(self.user, 'Cashew')

        res = self.client.get(INGREDIENT_LIST_URL)
        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredient_listing_limited_to_auth_user(self):
        '''test that returned ingredients belong to authenticated user'''
        user2 = create_sample_user(
            email='test2@domain.com', password='testpass1')
        create_ingredient(user2, 'Tomato')
        ingredient = create_ingredient(self.user, 'Carrot')

        res = self.client = self.client.get(INGREDIENT_LIST_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient.name)

    def test_create_ingredient_success(self):
        '''test creation of ingredient with correct data'''
        payload = {'name': 'New Ingredient'}
        res = self.client.post(INGREDIENT_LIST_URL, payload)

        exists = Ingredient.objects.filter(
            user=self.user, name=payload['name']).exists()

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(exists)

    def test_create_ingredient_invalid(self):
        '''test creation of ingredient with invalid data'''
        res = self.client.post(INGREDIENT_LIST_URL, {'name': ''})

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
