from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'autocomplete': 'name', 'required': True}),
            'email': forms.EmailInput(attrs={'autocomplete': 'email', 'required': True}),
            'phone': forms.TextInput(attrs={'autocomplete': 'tel'}),
            'message': forms.Textarea(attrs={'rows': 6, 'required': True}),
        }
        labels = {
            'name': 'Ime i prezime *',
            'email': 'Email *',
            'phone': 'Telefon',
            'message': 'Poruka *',
        }
