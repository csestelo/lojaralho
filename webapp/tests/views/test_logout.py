from django.contrib.sessions.models import Session
from django.core.urlresolvers import reverse
from django.test import TestCase

from webapp.views import logout
from webapp.tests.user_helpers import UserHelperMixin


class TestLogoutViewGET(UserHelperMixin, TestCase):
    def test_user_is_logged_out(self):
        password = '1234'
        self.create_authenticated_user(password)
        #  just to be sure, we check a session exists after the user logs in
        self.assertTrue(Session.objects.all())
        response = self.client.get(reverse('logout'))

        self.assertEqual(response.resolver_match.func, logout)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')
        self.assertFalse(Session.objects.all())

    def test_redirects_to_home_when_no_user_is_authenticated(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.resolver_match.func, logout)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')
        self.assertFalse(Session.objects.all())

