from django import forms

from .models import Cliente


class BootstrapForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for campo in self.fields.values():
            campo.widget.attrs["class"] = (
                "form-select" if isinstance(campo.widget, forms.Select) else "form-control"
            )


class ClienteForm(BootstrapForm):
    class Meta:
        model = Cliente
        fields = ["nome", "telefone", "email"]