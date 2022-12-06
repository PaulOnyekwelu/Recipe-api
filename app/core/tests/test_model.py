from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def create_sample_user(email='test@domain.com', password='testPass'):
    '''create and return a test user'''
    return get_user_model().objects.create_user(email, password)


class ModelTest(TestCase):
    '''test suite for models'''

    def test_create_user_with_email_successful(self):
        '''test successfully creation of users with email and password'''
        email = 'test@domain.com'
        password = 'TestPass123'
        user = get_user_model().objects.create_user(
            email=email, password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_create_user_email_is_normalized(self):
        '''test that the second part of user email is normalized'''
        email = 'test@DOMAIN.COM'
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        '''test that error is thrown if no email is provided'''
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_superuser(self):
        '''test the creation of superuser'''
        email = 'superuser@domain.com'
        password = 'TestPassword123'
        superuser = get_user_model().objects.create_superuser(email, password)

        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_tag_model_str(self):
        '''test tag model string representation'''
        tag = models.Tag.objects.create(
            user=create_sample_user(),
            name='Drinks'
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingredient_model_str(self):
        '''test ingredient model string representation'''
        ingredient = models.Ingredient.objects.create(
            user=create_sample_user(),
            name='Test Ingredient'
        )

        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_model_str(self):
        '''test recipe model string representation'''
        recipe = models.Recipe.objects.create(
            user=create_sample_user(),
            title='test recipe',
            time_minutes=10,
            price=9.99
        )

        self.assertEqual(str(recipe), recipe.title)

    @patch('uuid.uuid4')
    def test_upload_recipe_image_file_path(self, mock_patch):
        '''test that images are uploaded to correct path'''
        uuid_val = 'UUIDVALUE'
        mock_patch.return_value = uuid_val

        file_path = models.recipe_image_file_path(None, 'test_image.jpg')
        expected_path = f'uploads/recipe/{uuid_val}.jpg'

        self.assertEqual(file_path, expected_path)
