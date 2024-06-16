from django.contrib.auth import get_user_model
from django.test import TestCase
from model_bakery.baker import make

from authenticator.models import User


class UsersManagersTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email="testuser@mail.com", password="foobar")

        assert user.email == "testuser@mail.com"
        assert user.is_active
        assert not user.is_staff
        assert not user.is_superuser
        try:
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email="")
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="foobar")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            email="testsuperuser@mail.com", password="foobar"
        )

        assert admin_user.email == "testsuperuser@mail.com"
        assert admin_user.is_active
        assert admin_user.is_staff
        assert admin_user.is_superuser

        try:
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass

        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="testsuperuser@mail.com", password="foobar", is_staff=False
            )

        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="testsuperuser@mail.com", password="foobar", is_superuser=False
            )

    def test_user_string_representation(self):
        user = make(User)
        assert str(user) == user.email
