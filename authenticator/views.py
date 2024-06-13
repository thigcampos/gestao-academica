from django.views.generic import View
from django.contrib.auth import logout
from django.conf import settings
from django.http import HttpResponseRedirect


class LogoutView(View):

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(settings.LOGIN_URL)
