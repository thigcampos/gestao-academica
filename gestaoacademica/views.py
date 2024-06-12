from django.views.generic import TemplateView, ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect

from authenticator.forms import UserCreationForm
from authenticator.models import User
from gestaoacademica.models import Aluno, OfertaDisciplina, Participacao
from gestaoacademica.forms import AlunoForm


class AlunoHomeView(LoginRequiredMixin, TemplateView):
    model = Aluno
    login_url = "/accounts/login"
    template_name = "alunos/home.html"


class AlunoCreateView(CreateView):
    model = Aluno
    form_class = AlunoForm
    template_name = "alunos/create.html"
    success_url = reverse_lazy("alunos_home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = UserCreationForm
        return context

    def post(self, request, *args, **kwargs):
        user_email = request.POST.get("email")
        user_password = request.POST.get("password1")
        user = User.objects.create_user(user_email, user_password)

        aluno_nome = request.POST.get("nome")
        aluno_sobrenome = request.POST.get("sobrenome")
        aluno_prontuario = request.POST.get("prontuario")
        Aluno.objects.create(
            user=user,
            nome=aluno_nome,
            sobrenome=aluno_sobrenome,
            prontuario=aluno_prontuario,
        )
        return HttpResponseRedirect(self.success_url)


class OfertaDisciplinaListView(LoginRequiredMixin, ListView):
    login_url = "/accounts/login"
    model = OfertaDisciplina
    template_name = "disciplinas/list.html"
    queryset = OfertaDisciplina.objects.all()


class ParticipacaoUpdateView(LoginRequiredMixin, UpdateView):
    login_url = "/accounts/login"
    model = Participacao
    template_name = "disciplinas/list.html"
    success_url = reverse_lazy("alunos_home")
