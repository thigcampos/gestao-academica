from http import HTTPStatus
from django.urls import resolve, reverse
from django.contrib.auth import views as auth_views
from django.test import TestCase


class TestRoutesLogin(TestCase):
    def setUp(self):
        self._url = reverse("accounts_login")

    def test_url_resolves_to_view(self):
        resolved = resolve(self._url)
        assert resolved.func.view_class == auth_views.LoginView

    def test_loads_correct_view(self):
        response = self.client.get(self._url)
        assert response.status_code == HTTPStatus.OK
        self.assertTemplateUsed(response, "registration/login.html")
