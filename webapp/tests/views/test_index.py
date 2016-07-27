from django.test import TestCase
from webapp.views import index


class TestIndex(TestCase):
    def test_render_correct_template(self):
        response = self.client.get('/')
        template_names = [template.name for template in response.templates]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func, index)
        self.assertEqual(template_names, ['index.html'])
