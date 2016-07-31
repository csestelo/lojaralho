from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login as log_user_in
from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory
from model_mommy import mommy

from webapp.views import login
from webapp.models import User


import unittest
@unittest.skip
class TestIndex(TestCase):
    def test_render_correct_template(self):
        response = self.client.get(reverse('signup'))
        template_names = [template.name for template in response.templates]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func, signup)
        self.assertEqual(template_names, ['signup.html'])

    def test_valid_signup_redirects_to_welcome_page(self):
        post_data = {
            'email': 'arya@stark.com',
            'email_verify': 'arya@stark.com',
            'username': 'arya',
            'first_name': 'Arya',
            'last_name': 'Stark',
            'password1': 'carreta2000',
            'password2': 'carreta2000',
        }

        response = self.client.post(reverse('signup'), data=post_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], reverse('welcome'))


class LoginHelperMixin:
    def create_authenticated_user(self, password, **kwargs):
        user = self.create_user(password, **kwargs)
        logged_in = self.client.login(username=user.username,
                                      password=password)
        self.assertTrue(logged_in)
        return user

    def create_user(self, password, **kwargs):
        return mommy.make(User,
                          password=make_password(password),
                          _fill_optional=['email'],
                          **kwargs)


class TestLoginViewGET(LoginHelperMixin, TestCase):
    def test_redirect_to_welcome_if_user_is_authenticated(self):
        self.create_authenticated_user('12345')
        session_id = self.client.cookies['sessionid']
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.cookies['sessionid'], session_id)
        self.assertEqual(response['location'], reverse('welcome'))

    def test_correct_view_is_called_and_correct_template_is_rendered(self):
        response = self.client.get(reverse('login'))
        template_names = [template.name for template in response.templates]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func, login)
        self.assertEqual(template_names, ['login.html'])


class TestLoginViewPOST(LoginHelperMixin, TestCase):
    def test_post(self):
        password = '11234'
        user = self.create_user(password)
        data = {'username': user.username, 'password': password}

        response = self.client.post(reverse('login'), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.resolver_match.func, login)
        self.assertEqual(response['location'], reverse('welcome'))

    def test_redirect_to_welcome_if_user_is_authenticated(self):
        password = '12345'

        user = self.create_authenticated_user(password=password)
        data = {'username': user.username, 'password': password}
        session_id = self.client.cookies['sessionid']

        response = self.client.post(reverse('login'), data=data)
        self.assertEqual(self.client.cookies['sessionid'], session_id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], reverse('welcome'))

    def test_redirect_to_welcome_if_authenticated_user_impersonates_other(self):
        password = '12345'

        other_user = self.create_user(password)
        data = {'username': other_user.username, 'password': password}
        self.create_authenticated_user(password)

        session_id = self.client.cookies['sessionid']
        response = self.client.post(reverse('login'), data=data)
        self.assertEqual(self.client.cookies['sessionid'], session_id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], reverse('welcome'))

