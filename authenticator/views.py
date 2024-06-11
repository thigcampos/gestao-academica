from django_registration.forms import RegistrationForm

from authentication.models import User


class CustomUserForm(RegistrationForm):
    class Meta(RegistrationForm.Meta):
        model = User
