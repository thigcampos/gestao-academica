from django.views.generic import TemplateView, ListView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


class AlunoHomeView(LoginRequiredMixin, TemplateView):
    login_url = "/accounts/login"
    template_name = "alunos/home.html"


class DisciplinaListView(LoginRequiredMixin, ListView):
    login_url = "/accounts/login"
    # model = Disciplina
    template_name = "disciplinas/list.html"
    # queryset = Disciplina.object.all()

    # Remove that after Disciplina Model is created
    def get_queryset(self):
        return []


class ParticipacaoUpdateView(LoginRequiredMixin, UpdateView):
    login_url = "/accounts/login"
    # model = Participacao
    template_name = "disciplinas/list.html"
    success_url = reverse_lazy("alunos_home")

    # Remove that after Participacao Model is created
    def get_queryset(self):
        return []
