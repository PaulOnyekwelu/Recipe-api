from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe, Ingredient, Tag
from recipe.serializers import RecipeSerializer, RecipeDetailSerializer

RECIPE_LIST_URL = reverse('recipe:recipe-list')


def compute_recipe_detail_url(recipe_id):
    '''compute and return a recipe detail url'''
    return reverse('recipe:recipe-detail', args=[recipe_id])


def create_sample_user(**params):
    '''create and return a test user'''
    defaults = {
        'email': 'test@domain.com',
        'password': 'testPass'
    }
    defaults.update(params)
    return get_user_model().objects.create_user(**defaults)


def create_sample_ingredient(user, name='Butter'):
    '''create and return a sample ingredient'''
    return Ingredient.objects.create(user=user, name=name)


def create_sample_tag(user, name='Main'):
    '''create and return a sample tag'''
    return Tag.objects.create(user=user, name=name)


def create_sample_recipe(user, **params):
    '''create a sample recipe'''
    defaults = {
        'title': 'test recipe',
        'time_minutes': 5,
        'price': 10.00
    }
    defaults.update(params)

    return Recipe.objects.create(user=user, **defaults)


class PublicRecipeAPITest(TestCase):
    '''test suite for unauthenticated recipe api access'''

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        '''test that recipe endpoint is auth-protected'''
        res = self.client.get(RECIPE_LIST_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeAPITest(TestCase):
    '''test suite for authenticated recipe api access'''

    def setUp(self):
        self.user = create_sample_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_get_recipe_success(self):
        '''test that auth user can get recipe list'''
        create_sample_recipe(user=self.user)
        create_sample_recipe(user=self.user)

        res = self.client.get(RECIPE_LIST_URL)
        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_recipe_auth_user(self):
        '''test that returned recipes belong to auth user'''
        user2 = create_sample_user(email='user2@domain.com')

        create_sample_recipe(user=self.user)
        create_sample_recipe(user=user2)

        res = self.client.get(RECIPE_LIST_URL)

        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    def test_view_recipe_detail(self):
        '''test viewing recipe detail api endpoint'''
        recipe = create_sample_recipe(user=self.user)
        recipe.tags.add(create_sample_tag(user=self.user))
        recipe.ingredients.add(create_sample_ingredient(user=self.user))

        res = self.client.get(compute_recipe_detail_url(recipe.id))

        serializer = RecipeDetailSerializer(recipe)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_basic_recipe(self):
        '''test creating basic recipe'''
        payload = {
            'title': 'test recipe',
            'time_minutes': 5,
            'price': 4.00
        }
        res = self.client.post(RECIPE_LIST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recipe = Recipe.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(recipe, key))

    def test_create_recipe_with_tags(self):
        '''test create recipe with tags'''
        tag1 = create_sample_tag(user=self.user, name='Beef')
        tag2 = create_sample_tag(user=self.user, name='Vegan')

        payload = {
            'title': 'test recipe tags',
            'time_minutes': 5,
            'price': 99.00,
            'tags': [tag1.id, tag2.id]
        }

        res = self.client.post(RECIPE_LIST_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recipe = Recipe.objects.get(id=res.data['id'])
        tags = recipe.tags.all()
        self.assertEqual(tags.count(), 2)
        self.assertIn(tag1, tags)
        self.assertIn(tag2, tags)

    def test_create_recipe_with_ingredient(self):
        '''test create recipe with ingredients'''
        ingredient1 = create_sample_ingredient(user=self.user, name='Broccoli')
        ingredient2 = create_sample_ingredient(user=self.user, name='Cabbage')

        default = {
            'title': 'test recipe ingredient',
            'time_minutes': 60,
            'price': 20.00,
            'ingredients': [ingredient1.id, ingredient2.id]
        }

        res = self.client.post(RECIPE_LIST_URL, default)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recipes = Recipe.objects.get(id=res.data['id'])
        ingredients = recipes.ingredients.all()
        self.assertEqual(ingredients.count(), 2)
        self.assertIn(ingredient1, ingredients)
        self.assertIn(ingredient2,  ingredients)

    def test_update_recipe_patch(self):
        '''test updating recipe through http patch'''
        recipe = create_sample_recipe(user=self.user)
        recipe.tags.add(create_sample_tag(user=self.user))
        recipe.tags.add(create_sample_tag(user=self.user, name='Moves'))
        recipe.ingredients.add(create_sample_ingredient(user=self.user))

        new_tag = create_sample_tag(user=self.user, name='Goat Meat')
        payload = {
            'title': 'Egusi Soup',
            'tags': [new_tag.id]
        }

        self.client.patch(compute_recipe_detail_url(recipe.id), payload)

        recipe.refresh_from_db()
        self.assertEqual(recipe.title, payload['title'])
        tags = recipe.tags.all()
        self.assertEqual(len(tags), 1)
        self.assertIn(new_tag, tags)

    def test_update_recipe_put(self):
        '''test updating recipe through http put'''
        recipe = create_sample_recipe(user=self.user)
        recipe.tags.add(create_sample_tag(user=self.user))
        recipe.ingredients.add(create_sample_ingredient(user=self.user))

        payload = {
            'title': 'Nsala Soup',
            'time_minutes': 60,
            'price': 100.00
        }

        self.client.put(compute_recipe_detail_url(recipe.id), payload)

        recipe.refresh_from_db()
        tags = recipe.tags.all()
        ingredients = recipe.ingredients.all()
        self.assertEqual(recipe.title, payload['title'])
        self.assertEqual(recipe.time_minutes, payload['time_minutes'])
        self.assertEqual(recipe.price, payload['price'])
        self.assertEqual(len(tags), 0)
        self.assertEqual(len(ingredients), 0)
