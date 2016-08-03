from django.core.urlresolvers import reverse
from django.test import TestCase

from webapp.views import login
from webapp.tests.user_helpers import UserHelperMixin


class TestLoginViewGET(UserHelperMixin, TestCase):
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


class TestLoginViewPOST(UserHelperMixin, TestCase):
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

