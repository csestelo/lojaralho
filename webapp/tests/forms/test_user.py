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

    def test_all_fields(self):
        form = User(self.user_data)
        self.assertTrue(form.is_valid())

        user = form.save()
        self.assertEqual(user.email, self.user_data['email'])
        self.assertEqual(user.username, self.user_data['username'])
        self.assertEqual(user.first_name, self.user_data['first_name'])
        self.assertEqual(user.last_name, self.user_data['last_name'])
        self.assertTrue(check_password(self.user_data['password1'],
                                       user.password))
        self.assertEqual(user.address, self.user_data['address'])
        self.assertEqual(user.cellphone, self.user_data['cellphone'])

    def test_only_required_fields(self):
        del self.user_data['address']
        del self.user_data['cellphone']

        form = User(self.user_data)
        self.assertTrue(form.is_valid())

        user = form.save()
        self.assertEqual(user.email, self.user_data['email'])
        self.assertEqual(user.username, self.user_data['username'])
        self.assertEqual(user.first_name, self.user_data['first_name'])
        self.assertEqual(user.last_name, self.user_data['last_name'])
        self.assertTrue(check_password(self.user_data['password1'],
                                       user.password))
        self.assertEqual(user.address, '')
        self.assertEqual(user.cellphone, '')

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
