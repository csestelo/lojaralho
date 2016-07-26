from django.test import TestCase
from django.core.urlresolvers import resolve
from webapp.views import index


class TestUrlResolve(TestCase):
    def test_root_should_point_to_webapp_index(self):
        self.assertEqual(resolve('/').func, index)
