from django.test import Client, TestCase
from django.urls import reverse

from authenticator.models import User


class LogoutViewTest(TestCase):
    """Unit tests for LogoutView"""

    def setUp(self):
        """Create a logged-in user for testing"""
        self.user = User.objects.create_user(email="testuser@mail.com", password="secret")
        self.client = Client()
        self.client.login(email="testuser@mail.com", password="secret")

    def test_logout(self):
        """Test successful logout using the view"""
        url = reverse("accounts_logout")
        response = self.client.get(url)

        # Check for redirection and user being logged out
        assert response.status_code == 302
        assert not self.user == self.client.session.get('_auth_user')
