from django.views.generic import TemplateView, ListView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import views as auth_views

from authenticator.forms import UserCreationForm
from authenticator.models import User
from gestaoacademica.models import (
    Aluno,
    OfertaDisciplina,
    Participacao,
    Turma,
    Disciplina,
    ListaDeEspera,
)
from gestaoacademica.forms import AlunoForm

from django.views.generic.base import ContextMixin


class CommonContextMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_creation_form"] = UserCreationForm
        return context


class LoginPageView(auth_views.LoginView, CommonContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class HomePageView(LoginRequiredMixin, CommonContextMixin, TemplateView):
    model = Aluno
    login_url = "/accounts/login"
    template_name = "general/home.html"


class AlunoCreateView(CommonContextMixin, CreateView):
    model = Aluno
    form_class = AlunoForm
    template_name = "alunos/create.html"
    success_url = reverse_lazy("home_page")

    def post(self, request, *args, **kwargs):
        email = request.POST.get("email")
        password = request.POST.get("password1")
        user = User.objects.create_user(email, password)

        first_name = request.POST.get("nome")
        last_name = request.POST.get("sobrenome")
        registration_number = request.POST.get("prontuario")
        Aluno.objects.create(
            user=user,
            nome=first_name,
            sobrenome=last_name,
            prontuario=registration_number,
        )
        return HttpResponseRedirect(self.success_url)


class OfertaDisciplinaListView(LoginRequiredMixin, CommonContextMixin, ListView):
    login_url = "/accounts/login"
    model = OfertaDisciplina
    template_name = "disciplinas/list.html"
    queryset = OfertaDisciplina.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        aluno = Aluno.objects.filter(user=self.request.user).first()
        disciplinas_inscritas = Participacao.objects.filter(aluno=aluno)
        context["aluno"] = aluno
        context["disciplinas_inscritas"] = [
            participacao.ofertaDisciplina for participacao in disciplinas_inscritas
        ]
        return context


class ParticipacaoCreateView(LoginRequiredMixin, CommonContextMixin, CreateView):
    login_url = "/accounts/login"
    model = Participacao
    fields = ["aluno", "oferta_disciplina"]
    template_name = "disciplinas/list.html"
    success_url = reverse_lazy("home_page")
    failed_url = reverse_lazy("oferta_disciplina_list")

    def post(self, request, *args, **kwargs):
        oferta_ids = request.POST.getlist("oferta-disciplina")
        aluno = Aluno.objects.filter(user=self.request.user).first()
        conflito_agenda = []
        disciplinas_pendentes = []

        if len(oferta_ids) > 4:
            messages.error(request, "Créditos excedidos, máximo 20 (cada inscrição vale 5 créditos)")
            return HttpResponseRedirect(self.failed_url)

        if Participacao.objects.filter(aluno=aluno).count()*5 + len(oferta_ids)*5 >= 20:
            messages.error(request, "Créditos excedidos, máximo 20 (cada inscrição vale 5 créditos)")
            return HttpResponseRedirect(self.failed_url)

        if Participacao.objects.filter(aluno=aluno).exists():
            participacoes = Participacao.objects.filter(aluno=aluno)
            for participacao in participacoes:
                conflito_agenda.append(
                    f"{participacao.ofertaDisciplina.diaDaSemana}-{participacao.ofertaDisciplina.horarioInicio}"
                )

        for oferta_id in oferta_ids:
            oferta_disciplina = OfertaDisciplina.objects.filter(pk=oferta_id).first()

            if oferta_disciplina.disciplina.dependencia:
                dependencia = Disciplina.objects.filter(
                    nome=oferta_disciplina.disciplina.dependencia.nome
                ).first()
                if dependencia not in aluno.disciplinas_concluidas.all():
                    messages.error(
                        request,
                        f"A disciplina {oferta_disciplina.disciplina.nome} tem como pré-requisito {dependencia.nome}, a qual você não cursou",
                    )
                    return HttpResponseRedirect(self.failed_url)

            oferta_horario = (
                f"{oferta_disciplina.diaDaSemana}-{oferta_disciplina.horarioInicio}"
            )
            if oferta_horario in conflito_agenda:
                messages.error(request, "Há conflito de horários")
                return HttpResponseRedirect(self.failed_url)

            if (
                oferta_disciplina.sala.capacidade
                == oferta_disciplina.turma.aluno.count()
            ):
                disciplinas_pendentes.append(str(oferta_disciplina))
                continue

            conflito_agenda.append(oferta_horario)
            turma = Turma.objects.filter(pk=oferta_disciplina.turma.id).first()
            turma.aluno.add(aluno)
            turma.save()

            Participacao.objects.create(aluno=aluno, ofertaDisciplina=oferta_disciplina)

        if disciplinas_pendentes:
            request.session["disciplinas_pendentes"] = disciplinas_pendentes
            return HttpResponseRedirect(self.failed_url)

        messages.success(request, "Inscrição feita com sucesso")
        return HttpResponseRedirect(self.success_url)


class OtherParticipacaoCreateView(LoginRequiredMixin, CommonContextMixin, ListView):
    def post(self, request, *args, **kwargs):
        disciplina_pendente = request.POST.getlist("disciplina-pendente")[0]
        temp = request.session["disciplinas_pendentes"][:]
        temp.remove(disciplina_pendente)
        request.session["disciplinas_pendentes"] = temp
        return HttpResponseRedirect(reverse_lazy("oferta_disciplina_list"))


class ListaDeEsperaCreateView(LoginRequiredMixin, CommonContextMixin, ListView):
    def post(self, request, *args, **kwargs):
        disciplina_pendente = request.POST.getlist("disciplina-pendente")[0]
        temp = request.session["disciplinas_pendentes"][:]
        temp.remove(disciplina_pendente)
        request.session["disciplinas_pendentes"] = temp

        nome_disciplina = disciplina_pendente.split(" (")[0]
        disciplina = Disciplina.objects.filter(nome=nome_disciplina).first()
        oferta_disciplina = OfertaDisciplina.objects.filter(
            disciplina=disciplina
        ).first()
        aluno = Aluno.objects.filter(user=request.user).first()

        lista_de_espera, created = ListaDeEspera.objects.get_or_create(
            ofertaDisciplina=oferta_disciplina
        )
        lista_de_espera.aluno.add(aluno)

        if "lista_de_espera" in request.session:
            request.session["lista_de_espera"].append(str(oferta_disciplina))
        else:
            request.session["lista_de_espera"] = [str(oferta_disciplina)]

        messages.success(request, "Aluno inserido na lista de espera!")
        return HttpResponseRedirect(reverse_lazy("oferta_disciplina_list"))


class AlunoDisciplinaListView(LoginRequiredMixin, CommonContextMixin, ListView):
    login_url = "/accounts/login"
    model = OfertaDisciplina
    template_name = "alunos/list.html"
    queryset = Participacao.objects.all()

    def get_queryset(self):
        aluno = Aluno.objects.filter(user=self.request.user).first()
        participacoes = Participacao.objects.filter(aluno=aluno)
        return [participacao.ofertaDisciplina for participacao in participacoes]


class ParticipacaoDeleteView(LoginRequiredMixin, CommonContextMixin, ListView):
    def post(self, request, *args, **kwargs):
        nome_disciplina = request.POST.getlist("disciplina-solicitada")[0]
        disciplina = Disciplina.objects.filter(nome=nome_disciplina).first()

        oferta_disciplina = OfertaDisciplina.objects.filter(
            disciplina=disciplina
        ).first()
        aluno = Aluno.objects.filter(user=request.user).first()

        participacao = Participacao.objects.filter(
            ofertaDisciplina=oferta_disciplina, aluno=aluno
        ).first()
        participacao.delete()
        messages.success(request, "Inscrição cancelada com sucesso!")
        return HttpResponseRedirect(reverse_lazy("aluno_disciplina_list"))


class ListaDeEsperaDeleteView(LoginRequiredMixin, CommonContextMixin, ListView):
    def post(self, request, *args, **kwargs):
        disciplina_solicitada = request.POST.getlist("disciplina-solicitada")[0]
        nome_disciplina = disciplina_solicitada.split(" (")[0]

        disciplina = Disciplina.objects.filter(nome=nome_disciplina).first()
        oferta_disciplina = OfertaDisciplina.objects.filter(
            disciplina=disciplina
        ).first()
        aluno = Aluno.objects.filter(user=request.user).first()

        lista_de_espera = ListaDeEspera.objects.filter(
            ofertaDisciplina=oferta_disciplina, aluno=aluno
        ).first()
        lista_de_espera.delete()
        temp = request.session["lista_de_espera"][:]
        temp.remove(disciplina_solicitada)
        request.session["lista_de_espera"] = temp
        messages.success(request, "Inscrição na lista de espera cancelada com sucesso!")
        return HttpResponseRedirect(reverse_lazy("aluno_disciplina_list"))
