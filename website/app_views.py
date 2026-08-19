from datetime import datetime
from decimal import Decimal
from functools import wraps

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST

from .forms import AppLoginForm, ArticleForm, PartnerForm
from .models import Article, ContactMessage, Partner


def owner_required(view):
    @login_required
    @wraps(view)
    def wrapped(request, *args, **kwargs):
        if not request.user.is_staff:
            logout(request)
            return redirect('app_login')
        return view(request, *args, **kwargs)

    return wrapped


def _safe_next(request):
    candidate = request.POST.get('next') or request.GET.get('next') or ''
    if candidate and url_has_allowed_host_and_scheme(
        candidate,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return candidate
    return ''


def _app_context(request, title, **extra):
    return {
        'seo': {'title': f'{title} | Food Compass'},
        'app_unread': ContactMessage.objects.filter(is_read=False).count(),
        **extra,
    }


@never_cache
def app_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect(_safe_next(request) or 'app_home')

    form = AppLoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        if not user.is_staff:
            form.add_error(None, 'Ovaj nalog nema pristup panelu.')
        else:
            login(request, user)
            return redirect(_safe_next(request) or 'app_home')

    return render(request, 'app/login.html', {
        'form': form,
        'next': _safe_next(request),
        'seo': {'title': 'Prijava | Food Compass'},
    })


@require_POST
def app_logout(request):
    logout(request)
    return redirect('home')


@owner_required
def app_home(request):
    messages = ContactMessage.objects.all()[:6]
    articles = Article.objects.all()[:5]
    return render(request, 'app/home.html', _app_context(
        request,
        'Pregled',
        recent_messages=messages,
        recent_articles=articles,
        message_count=ContactMessage.objects.count(),
        article_count=Article.objects.filter(is_published=True).count(),
        partner_count=Partner.objects.count(),
    ))


@owner_required
def app_messages(request):
    return render(request, 'app/messages.html', _app_context(
        request,
        'Poruke',
        contact_messages=ContactMessage.objects.all(),
    ))


@owner_required
def app_message_detail(request, pk):
    message = get_object_or_404(ContactMessage, pk=pk)
    if not message.is_read:
        message.is_read = True
        message.save(update_fields=['is_read'])
    return render(request, 'app/message_detail.html', _app_context(
        request,
        message.name,
        message=message,
    ))


@owner_required
def app_news(request):
    return render(request, 'app/news.html', _app_context(
        request,
        'Aktuelnosti',
        articles=Article.objects.all(),
    ))


def _save_article(request, instance=None):
    form = ArticleForm(request.POST or None, request.FILES or None, instance=instance)
    if request.method == 'POST' and form.is_valid():
        article = form.save()
        toast = 'saved' if instance else 'created'
        url = reverse('app_news_detail', kwargs={'pk': article.pk})
        return redirect(f'{url}?toast={toast}')
    return form


@owner_required
def app_news_create(request):
    form = _save_article(request)
    if not isinstance(form, ArticleForm):
        return form
    return render(request, 'app/news_form.html', _app_context(
        request,
        'Nova vest',
        form=form,
        is_create=True,
    ))


@owner_required
def app_news_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'app/news_detail.html', _app_context(
        request,
        article.title,
        article=article,
    ))


@owner_required
def app_news_edit(request, pk):
    article = get_object_or_404(Article, pk=pk)
    form = _save_article(request, article)
    if not isinstance(form, ArticleForm):
        return form
    return render(request, 'app/news_form.html', _app_context(
        request,
        f'Izmena — {article.title}',
        form=form,
        article=article,
        is_create=False,
    ))


def _parse_date(value):
    if not value:
        return None
    try:
        return datetime.strptime(value, '%Y-%m-%d').date()
    except ValueError:
        return None


def _partner_queryset(request):
    query = request.GET.get('q', '').strip()
    status = request.GET.get('status', '').strip()
    date_from = _parse_date(request.GET.get('from', '').strip())
    date_to = _parse_date(request.GET.get('to', '').strip())
    partners = Partner.objects.all()
    if query:
        status_matches = [
            code for code, label in Partner.STATUS_CHOICES
            if query.casefold() in label.casefold() or query.casefold() in code.casefold()
        ]
        lookup = Q(name__icontains=query) | Q(description__icontains=query)
        if status_matches:
            lookup |= Q(status__in=status_matches)
        partners = partners.filter(lookup)
    if status:
        partners = partners.filter(status=status)
    if date_from:
        partners = partners.filter(recorded_on__gte=date_from)
    if date_to:
        partners = partners.filter(recorded_on__lte=date_to)
    return partners, query, status, date_from, date_to


@owner_required
def app_partners(request):
    partners, query, status, date_from, date_to = _partner_queryset(request)
    paginator = Paginator(partners, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    page_numbers = page_obj.paginator.get_elided_page_range(
        page_obj.number, on_each_side=1, on_ends=1
    )
    params = request.GET.copy()
    params.pop('page', None)
    total_all = Partner.objects.aggregate(total=Sum('amount'))['total'] or Decimal('0')
    total_filtered = partners.aggregate(total=Sum('amount'))['total'] or Decimal('0')
    filters_active = bool(query or status or date_from or date_to)
    return render(request, 'app/partners.html', _app_context(
        request,
        'Saradnja',
        page_obj=page_obj,
        page_numbers=page_numbers,
        query=query,
        status_filter=status,
        date_from=date_from.isoformat() if date_from else '',
        date_to=date_to.isoformat() if date_to else '',
        query_string=params.urlencode(),
        status_choices=Partner.STATUS_CHOICES,
        result_count=paginator.count,
        total_all_display=Partner.format_amount(total_all),
        total_filtered_display=Partner.format_amount(total_filtered),
        filters_active=filters_active,
    ))


def _save_partner(request, instance=None):
    form = PartnerForm(request.POST or None, instance=instance)
    if request.method == 'POST' and form.is_valid():
        partner = form.save()
        toast = 'saved' if instance else 'created'
        url = reverse('app_partner_detail', kwargs={'pk': partner.pk})
        return redirect(f'{url}?toast={toast}')
    return form


@owner_required
def app_partner_create(request):
    form = _save_partner(request)
    if not isinstance(form, PartnerForm):
        return form
    return render(request, 'app/partner_form.html', _app_context(
        request,
        'Novi unos',
        form=form,
        is_create=True,
    ))


@owner_required
def app_partner_detail(request, pk):
    partner = get_object_or_404(Partner, pk=pk)
    return render(request, 'app/partner_detail.html', _app_context(
        request,
        partner.name,
        partner=partner,
    ))


def app_partner_detail_redirect(request, pk):
    return redirect('app_partner_detail', pk=pk)


def app_partner_edit_redirect(request, pk):
    return redirect('app_partner_edit', pk=pk)


@owner_required
def app_partner_edit(request, pk):
    partner = get_object_or_404(Partner, pk=pk)
    form = _save_partner(request, partner)
    if not isinstance(form, PartnerForm):
        return form
    return render(request, 'app/partner_form.html', _app_context(
        request,
        f'Izmena — {partner.name}',
        form=form,
        partner=partner,
        is_create=False,
    ))
