from django.views.generic import TemplateView, ListView


class AlunoHomeView(TemplateView):
    template_name = "alunos/home.html"


class DisciplinaListView(ListView):
    template_name = "disciplinas/list.html"

    def get_queryset(self):
        return []
