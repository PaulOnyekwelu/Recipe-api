from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class TestAdmin(TestCase):
    '''test suite for the admin site'''

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='superuser@domain.com', password='test123'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='user@domain.com', password='test123', name='Test User'
        )

    def test_user_changelist_page(self):
        '''test that users are listed in the admin user page'''
        url = reverse('admin:core_authuser_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        '''test that user editpage works'''
        url = reverse('admin:core_authuser_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_user_add_page(self):
        '''test that add user page works'''
        url = reverse('admin:core_authuser_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
