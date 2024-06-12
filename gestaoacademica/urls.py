"""
URL configuration for gestaoacademica project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

from authenticator.views import UserCreateView, LogoutView
from gestaoacademica.views import (
    AlunoHomeView,
    OfertaDisciplinaListView,
    ParticipacaoUpdateView,
    AlunoCreateView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/register/", UserCreateView.as_view(), name="accounts_register"),
    path("accounts/login/", auth_views.LoginView.as_view(), name="accounts_login"),
    path("accounts/logout/", LogoutView.as_view(), name="accounts_logout"),
    path("accounts/register/aluno/", AlunoCreateView.as_view(), name="alunos_create"),
    path("", AlunoHomeView.as_view(), name="alunos_home"),
    path(
        "disciplinas/",
        OfertaDisciplinaListView.as_view(),
        name="oferta_disciplina_list",
    ),
    path(
        "alunos/<int:pk>/participacao/",
        ParticipacaoUpdateView.as_view(),
        name="participacao_update",
    ),
]
