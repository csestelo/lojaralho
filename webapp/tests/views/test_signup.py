from django.core.urlresolvers import reverse
from django.test import TestCase
from webapp.views import signup


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
