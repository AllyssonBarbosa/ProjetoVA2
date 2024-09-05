from django import forms
from .models import Produto

from django import forms
from .models import Produto

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'valor', 'quantidade', 'descricao','foto']


