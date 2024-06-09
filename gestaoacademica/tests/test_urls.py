from http import HTTPStatus
from django.urls import resolve, reverse
from django.contrib.auth import views as auth_views
from django.test import TestCase

from gestaoacademica.views import AlunoHomeView, DisciplinaListView


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


class TestRoutesHome(TestCase):
    def setUp(self):
        self._url = reverse("alunos_home")

    def test_url_resolves_to_view(self):
        resolved = resolve(self._url)
        assert resolved.func.view_class == AlunoHomeView

    def test_loads_correct_view(self):
        response = self.client.get(self._url)
        assert response.status_code == HTTPStatus.OK
        self.assertTemplateUsed(response, "alunos/home.html")


class TestRoutesCourses(TestCase):
    def setUp(self):
        self._url = reverse("disciplinas_list")

    def test_url_resolves_to_view(self):
        resolved = resolve(self._url)
        assert resolved.func.view_class == DisciplinaListView

    def test_loads_correct_view(self):
        response = self.client.get(self._url)
        assert response.status_code == HTTPStatus.OK
        self.assertTemplateUsed(response, "disciplinas/list.html")
