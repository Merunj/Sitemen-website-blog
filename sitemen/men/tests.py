from http import HTTPStatus
from http.client import responses

from django.test import TestCase
from django.urls import reverse

from men.models import Men


class GetPagesTestCase(TestCase):
    fixtures = ['men_men.json', 'men_category.json', 'men_tagpost.json']

    def setUp(self):
        "Инициализация перед выполнением каждого теста"

    def test_mainpage(self):
        path = reverse('home')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        # self.assertIn('men/index.html', response.template_name)
        self.assertTemplateUsed(response, 'men/index.html')
        self.assertEqual(response.context_data['title'], 'Главная страница')

    def test_redirect_addpage(self):
        path = reverse('add_page')
        redirect_uri = reverse('users:login') + '?next=' + path
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, redirect_uri)

    def test_data_mainpage(self):
        m = Men.published.get(pk=1)
        path = reverse('post', args=[m.slug])
        response = self.client.get(path)
        self.assertEqual(m.content, response.context_data['post'].content)

    # def test_content_post(self):
    #     m = Men.published.all().select_related('cat')
    #     path = reverse('home')
    #     response = self.client.get(path)
    #     self.assertQuerySetEqual(response.context_data['content'], m)

    def tearDown(self):
        "Действия после выполнения каждого теста"
