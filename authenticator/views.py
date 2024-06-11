from django.views.generic import FormView

from .forms import UserCreationForm


class UserCreateView(FormView):
    form_class = UserCreationForm
