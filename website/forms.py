from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils import timezone
from .models import Article, ContactMessage, Partner


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .copy_loader import site_copy

        strings = site_copy().STRINGS
        self.fields['name'].label = strings['form_name']
        self.fields['email'].label = strings['form_email']
        self.fields['phone'].label = strings['form_phone']
        self.fields['message'].label = strings['form_message']


class AppLoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login': 'Pogrešno korisničko ime ili lozinka.',
        'inactive': 'Ovaj nalog nije aktivan.',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Korisničko ime'
        self.fields['password'].label = 'Lozinka'
        self.fields['username'].widget.attrs.update({
            'autocomplete': 'username',
            'autofocus': True,
        })
        self.fields['password'].widget.attrs.update({
            'autocomplete': 'current-password',
        })


class PartnerForm(forms.ModelForm):
    class Meta:
        model = Partner
        fields = ['name', 'recorded_on', 'amount', 'description', 'status']
        widgets = {
            'name': forms.TextInput(attrs={'autocomplete': 'organization'}),
            'recorded_on': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'amount': forms.NumberInput(attrs={'step': '0.01', 'min': '0', 'inputmode': 'decimal'}),
            'description': forms.Textarea(attrs={'rows': 5}),
        }
        labels = {
            'name': 'Naziv saradnika',
            'recorded_on': 'Datum',
            'amount': 'Iznos',
            'description': 'Opis',
            'status': 'Status',
        }
        help_texts = {
            'amount': 'Iznos u RSD, npr. 15000.00',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['recorded_on'].input_formats = ['%Y-%m-%d']
        if not self.instance.pk:
            self.fields['recorded_on'].initial = timezone.localdate()


class ArticleForm(forms.ModelForm):
    remove_cover = forms.BooleanField(required=False, label='Ukloni sliku')

    class Meta:
        model = Article
        fields = [
            'title', 'excerpt', 'body',
            'title_en', 'excerpt_en', 'body_en',
            'title_ru', 'excerpt_ru', 'body_ru',
            'cover', 'is_published',
        ]
        widgets = {
            'title': forms.TextInput(),
            'excerpt': forms.Textarea(attrs={'rows': 3}),
            'body': forms.Textarea(attrs={'rows': 16, 'id': 'id_body'}),
            'title_en': forms.TextInput(),
            'excerpt_en': forms.Textarea(attrs={'rows': 3}),
            'body_en': forms.Textarea(attrs={'rows': 14, 'id': 'id_body_en'}),
            'title_ru': forms.TextInput(),
            'excerpt_ru': forms.Textarea(attrs={'rows': 3}),
            'body_ru': forms.Textarea(attrs={'rows': 14, 'id': 'id_body_ru'}),
            'cover': forms.FileInput(attrs={'accept': 'image/*'}),
        }
        labels = {
            'title': 'Naslov',
            'excerpt': 'Kratak opis',
            'body': 'Tekst',
            'title_en': 'Naslov',
            'excerpt_en': 'Kratak opis',
            'body_en': 'Tekst',
            'title_ru': 'Naslov',
            'excerpt_ru': 'Kratak opis',
            'body_ru': 'Tekst',
            'cover': 'Slika',
            'is_published': 'Objavi na sajtu',
        }
        help_texts = {
            'excerpt': 'Prikazuje se na listi aktuelnosti i na početnoj.',
            'cover': 'Prikazuje se na listi, na početnoj i u headeru vesti.',
            'is_published': 'Ako nije označeno, vest ostaje kao nacrt.',
            'title_en': 'Ako je prazno, na engleskom sajtu se prikazuje srpski naslov.',
            'title_ru': 'Ako je prazno, na ruskom sajtu se prikazuje srpski naslov.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not (self.instance.pk and self.instance.cover):
            self.fields.pop('remove_cover')

    def save(self, commit=True):
        article = super().save(commit=False)
        if self.cleaned_data.get('remove_cover') and not self.files.get('cover'):
            if article.cover:
                article.cover.delete(save=False)
            article.cover = ''
        if commit:
            article.save()
        return article
