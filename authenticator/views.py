from django.views.generic import FormView, View
from django.contrib.auth import logout
from django.conf import settings
from django.http import HttpResponseRedirect

from .forms import UserCreationForm


class UserCreateView(FormView):
    template_name = "registration/create.html"
    success_url = "/"
    form_class = UserCreationForm


class LogoutView(View):

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(settings.LOGIN_URL)
