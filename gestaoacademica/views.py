from django.views.generic import TemplateView, ListView, FormView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from gestaoacademica.models import Aluno, Disciplina, Participacao
from gestaoacademica.forms import AlunoForm


class AlunoHomeView(LoginRequiredMixin, TemplateView):
    model = Aluno
    login_url = "/accounts/login"
    template_name = "alunos/home.html"


class AlunoCreateView(FormView):
    form_class = AlunoForm
    template_name = "alunos/create.html"
    success_url = reverse_lazy("accounts_register")


class DisciplinaListView(LoginRequiredMixin, ListView):
    login_url = "/accounts/login"
    model = Disciplina
    template_name = "disciplinas/list.html"
    queryset = Disciplina.objects.all()


class ParticipacaoUpdateView(LoginRequiredMixin, UpdateView):
    login_url = "/accounts/login"
    model = Participacao
    template_name = "disciplinas/list.html"
    success_url = reverse_lazy("alunos_home")
