from django.test import TestCase
from django.contrib.auth import get_user_model


class TestModels(TestCase):
    '''test cases for models'''

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
