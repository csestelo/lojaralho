from django.core.urlresolvers import reverse
from django.test import TestCase
from webapp.views import welcome


class TestIndex(TestCase):
    def test_render_correct_template(self):
        response = self.client.get(reverse('welcome'))
        template_names = [template.name for template in response.templates]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func, welcome)
        self.assertEqual(template_names, ['index.html'])
