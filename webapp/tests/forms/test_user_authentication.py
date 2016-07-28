from django.contrib.auth.hashers import make_password
from django.test.testcases import TestCase
from model_mommy import mommy

from webapp.forms import UserAuthenticationForm
from webapp.models import User


class TestUserAuthenticationForm(TestCase):
    def test_form_valid(self):
        self.user = mommy.make(User,
                               username='Elias',
                               password=make_password('Stout6789'))

        correct_user_data = {'username': 'Elias', 'password': 'Stout6789'}
        form = UserAuthenticationForm(data=correct_user_data)
        self.assertTrue(form.is_valid())

        incorrect_user_data_username = {'username': 'Peluda',
                                        'password': 'Stout6789'}
        form = UserAuthenticationForm(data=incorrect_user_data_username)
        self.assertFalse(form.is_valid())

        incorrect_user_data_password = {'username': 'Peluda',
                                        'password': 'Standard6789'}
        form = UserAuthenticationForm(data=incorrect_user_data_password)
        self.assertFalse(form.is_valid())
