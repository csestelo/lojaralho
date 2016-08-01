from django.contrib.auth.hashers import make_password
from model_mommy import mommy

from webapp.models import User


class UserHelperMixin:
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

