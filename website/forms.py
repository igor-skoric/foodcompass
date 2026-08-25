from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms import inlineformset_factory
from django.utils import timezone
from .images import ImageProcessingError, normalize_cover
from .models import Article, ContactMessage, Partner, PartnerPayment
from .translate import fill_empty_translations

CONTACT_MESSAGE_MAX_LENGTH = 5000


class ContactForm(forms.ModelForm):
    message = forms.CharField(
        max_length=CONTACT_MESSAGE_MAX_LENGTH,
        widget=forms.Textarea(attrs={
            'rows': 6,
            'required': True,
            'maxlength': str(CONTACT_MESSAGE_MAX_LENGTH),
        }),
    )

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'autocomplete': 'name', 'required': True}),
            'email': forms.EmailInput(attrs={'autocomplete': 'email', 'required': True}),
            'phone': forms.TextInput(attrs={'autocomplete': 'tel'}),
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

        copy = site_copy()
        strings = copy.STRINGS
        self.fields['name'].label = strings['form_name']
        self.fields['email'].label = strings['form_email']
        self.fields['phone'].label = strings['form_phone']
        self.fields['message'].label = strings['form_message']
        self.fields['message'].error_messages['max_length'] = (
            copy.CONTACT_PAGE['form_message_too_long']
        )


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
        fields = ['name', 'recorded_on', 'due_on', 'description', 'status']
        widgets = {
            'name': forms.TextInput(attrs={'autocomplete': 'organization'}),
            'recorded_on': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'due_on': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'name': 'Naziv klijenta',
            'recorded_on': 'Datum',
            'due_on': 'Rok',
            'description': 'Opis',
            'status': 'Status',
        }
        help_texts = {
            'due_on': 'Ako rok prođe, status automatski postaje „Kasni sa plaćanjem“.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['recorded_on'].input_formats = ['%Y-%m-%d']
        self.fields['due_on'].input_formats = ['%Y-%m-%d']
        self.fields['due_on'].required = False
        if not self.instance.pk:
            today = timezone.localdate()
            self.fields['recorded_on'].initial = today
            self.fields['due_on'].initial = today


class PartnerPaymentForm(forms.ModelForm):
    class Meta:
        model = PartnerPayment
        fields = ['amount', 'paid_on', 'note']
        widgets = {
            'amount': forms.NumberInput(attrs={'step': '0.01', 'min': '0', 'inputmode': 'decimal'}),
            'paid_on': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'note': forms.TextInput(),
        }
        labels = {
            'amount': 'Iznos',
            'paid_on': 'Datum rate',
            'note': 'Napomena',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['paid_on'].input_formats = ['%Y-%m-%d']
        self.fields['amount'].required = False
        self.fields['paid_on'].required = False
        if not self.instance.pk:
            self.fields['paid_on'].initial = timezone.localdate()

    def has_changed(self):
        if self.instance.pk:
            return super().has_changed()
        if self.is_bound:
            raw = (self.data.get(self.add_prefix('amount')) or '').strip()
            if not raw:
                return False
        return super().has_changed()

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('DELETE'):
            return cleaned
        amount = cleaned.get('amount')
        if amount is not None and amount <= 0:
            self.add_error('amount', 'Iznos mora biti veći od nule.')
            return cleaned
        if amount and not cleaned.get('paid_on'):
            cleaned['paid_on'] = timezone.localdate()
        return cleaned


PartnerPaymentFormSet = inlineformset_factory(
    Partner,
    PartnerPayment,
    form=PartnerPaymentForm,
    extra=1,
    can_delete=True,
    min_num=0,
    max_num=40,
)


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
            'excerpt': 'Na karticama se prikazuju najviše 3 reda; duži tekst se skraćuje sa …',
            'cover': 'Najbolje 1600 × 900 px (16:9, pejzaž). Ista slika ide na početnu, listu i header vesti.',
            'is_published': 'Ako nije označeno, vest ostaje kao nacrt.',
            'title_en': 'Ako ostane prazno, popuniće se automatski pri čuvanju. Možete da korigujete prevod.',
            'title_ru': 'Ako ostane prazno, popuniće se automatski pri čuvanju. Možete da korigujete prevod.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not (self.instance.pk and self.instance.cover):
            self.fields.pop('remove_cover')

    def clean_cover(self):
        cover = self.cleaned_data.get('cover')
        uploaded = self.files.get('cover')
        if not uploaded:
            return cover
        try:
            return normalize_cover(uploaded)
        except ImageProcessingError as exc:
            raise forms.ValidationError(str(exc)) from exc

    def save(self, commit=True):
        article = super().save(commit=False)
        if self.cleaned_data.get('remove_cover') and not self.files.get('cover'):
            if article.cover:
                article.cover.delete(save=False)
            article.cover = ''
        self.auto_translated = fill_empty_translations(article)
        if commit:
            article.save()
        return article
