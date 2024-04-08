from django import forms
from .models import Filme, Genero

class FormFilme(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['genero'].queryset = Genero.objects.filter(user=self.user)
    
    class Meta:
        model = Filme
        fields = ['nome', 'duracao', 'data_de_lancamento', 'cartaz', 'genero']

    def save(self, commit=True, user=None):
        product = super().save(commit=False)
        product.user = user
        if commit:
            product.save()
        return product
    
class FormGenero(forms.ModelForm):
    class Meta:
        model = Genero
        fields = ['nome']

    def save(self, commit=True, user=None):
        genero = super().save(commit=False)
        genero.user = user
        if commit:
            genero.save()
        return genero