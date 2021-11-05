from django.test import TestCase
from django.shortcuts import reverse

# Create your tests here.

class CommonTests(TestCase):

    def test_index_page_url(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='common/index.html')

    def test_index_page_view_name(self):
        response = self.client.get(reverse('common:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='common/index.html')
