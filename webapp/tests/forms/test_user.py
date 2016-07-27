from django.contrib.auth.hashers import check_password
from django.test import TestCase

from webapp.forms import User


class TestUserForm(TestCase):
    def setUp(self):
        self.user_data = {
            'email': 'arya@stark.com',
            'email_verify': 'arya@stark.com',
            'username': 'arya',
            'first_name': 'Arya',
            'last_name': 'Stark',
            'password1': 'carreta2000',
            'password2': 'carreta2000',
            'address': 'Bravos Bay',
            'cellphone': '34567890'
        }

    def assert_user_matches(self, user, **expected_fields):
        self.assertEqual(user.email, expected_fields['email'])
        self.assertEqual(user.username, expected_fields['username'])
        self.assertEqual(user.first_name, expected_fields['first_name'])
        self.assertEqual(user.last_name, expected_fields['last_name'])
        self.assertTrue(check_password(expected_fields['password1'],
                                       user.password))
        self.assertEqual(user.address, expected_fields['address'])
        self.assertEqual(user.cellphone, expected_fields['cellphone'])

    def test_all_fields(self):
        form = User(self.user_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assert_user_matches(user, **self.user_data)

    def test_only_required_fields(self):
        del self.user_data['address']
        del self.user_data['cellphone']

        form = User(self.user_data)
        self.assertTrue(form.is_valid())

        user = form.save()
        self.assert_user_matches(user,
                                 address='',
                                 cellphone='',
                                 **self.user_data)

    def test_unique_fields(self):
        form = User(self.user_data)
        form.is_valid()
        form.save()

        # check *username* uniqueness
        user_data = self.user_data.copy()
        user_data['email'] = user_data['email_verify'] = 'sansa@stark.com'
        form = User(user_data)
        self.assertFalse(form.is_valid())

        # check *email* uniqueness
        user_data['username'] = 'melisandre'
        self.assertFalse(form.is_valid())

    def test_confirmation_fields(self):
        # check email confirmation
        form = User(dict(self.user_data,
                         email_verify='sansa@stark.com'))
        self.assertFalse(form.is_valid())

        # check password confirmation
        form = User(dict(self.user_data,
                         password2='321'))
        self.assertFalse(form.is_valid())
