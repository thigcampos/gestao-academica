from django import forms

from gestaoacademica.models import Aluno


class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ["nome", "sobrenome", "registroAluno"]

        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "sobrenome": forms.TextInput(attrs={"class": "form-control"}),
            "registroAluno": forms.TextInput(attrs={"class": "form-control"}),
        }
