from django import forms
from .models import Livro
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

class LivroForm(forms.ModelForm):
    class Meta:
        model = Livro
        fields = '__all__'
def __init__(self, *args, **kwargs):
    super(LivroForm, self).__init__(*args, **kwargs)
    self.helper = FormHelper()
    self.helper.layout = Layout(
        'titulo',
        'autor',
        'editora',
        'genero',
        'preco',
        'data_pub',
        'status',
        Submit('submit', 'Salvar')
    )