from django import forms

from gestaoacademica.models import Aluno


class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ["nome", "sobrenome", "registro_aluno"]

        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "sobrenome": forms.TextInput(attrs={"class": "form-control"}),
            "registro_aluno": forms.TextInput(attrs={"class": "form-control"}),
        }
