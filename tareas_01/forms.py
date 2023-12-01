from django import forms
from .models import Tareas

class formTareas(forms.ModelForm):
    class Meta:
        model = Tareas
        fields = ['titulo', 'descripcion', 'urgente']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Esbriba el título'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describa el problema'}),
            'urgente': forms.CheckboxInput(attrs={'class': 'form-check-input m-auto'})
        }