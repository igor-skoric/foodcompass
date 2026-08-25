import json
from datetime import datetime, timedelta
from functools import wraps

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST

from .forms import AppLoginForm, ArticleForm, PartnerForm, PartnerPaymentFormSet
from .models import Article, ContactMessage, Partner
from .translate import TranslationError, translate_article


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
    Partner.mark_overdue()
    today = timezone.localdate()
    soon = today + timedelta(days=14)
    partners = Partner.objects.all()
    late = partners.filter(status=Partner.STATUS_LATE)
    due_soon = partners.filter(
        due_on__gte=today,
        due_on__lte=soon,
    ).exclude(status=Partner.STATUS_COMPLETED).order_by('due_on', 'name')
    late_list = late.order_by('due_on', 'name')[:8]
    total = partners.aggregate(count=Count('id'))
    money = Partner.money_totals(partners)
    return render(request, 'app/home.html', _app_context(
        request,
        'Pregled',
        partner_count=total['count'] or 0,
        total_amount_display=Partner.format_amount(money['agreed']),
        paid_amount_display=Partner.format_amount(money['paid']),
        owed_amount_display=Partner.format_amount(money['owed']),
        late_count=late.count(),
        due_soon_count=due_soon.count(),
        active_count=partners.filter(status=Partner.STATUS_ACTIVE).count(),
        pending_count=partners.filter(status=Partner.STATUS_PENDING).count(),
        completed_count=partners.filter(status=Partner.STATUS_COMPLETED).count(),
        late_partners=late_list,
        due_soon_partners=due_soon[:8],
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
        if getattr(form, 'auto_translated', None):
            toast = 'translated'
        url = reverse('app_news_detail', kwargs={'pk': article.pk})
        return redirect(f'{url}?toast={toast}')
    return form


@owner_required
@require_POST
def app_news_translate(request):
    try:
        payload = json.loads(request.body.decode('utf-8') or '{}')
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Neispravan zahtev.'}, status=400)
    if not isinstance(payload, dict):
        return JsonResponse({'error': 'Neispravan zahtev.'}, status=400)
    title = payload.get('title') or ''
    excerpt = payload.get('excerpt') or ''
    body = payload.get('body') or ''
    if not isinstance(title, str) or not isinstance(excerpt, str) or not isinstance(body, str):
        return JsonResponse({'error': 'Neispravan zahtev.'}, status=400)
    try:
        result = translate_article(title, excerpt, body)
    except TranslationError as exc:
        return JsonResponse({'error': str(exc)}, status=502)
    return JsonResponse(result)


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


def _delete_article_files(article):
    if article.cover:
        article.cover.delete(save=False)
    if article.header_image:
        article.header_image.delete(save=False)
    for image in article.images.all():
        if image.image:
            image.image.delete(save=False)


@owner_required
@require_POST
def app_news_delete(request, pk):
    article = get_object_or_404(Article, pk=pk)
    _delete_article_files(article)
    article.delete()
    return redirect(f"{reverse('app_news')}?toast=deleted")


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
    partners = Partner.objects.annotate(payment_count=Count('payments'))
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
    return partners.order_by('-recorded_on', 'name'), query, status, date_from, date_to


@owner_required
def app_partners(request):
    Partner.mark_overdue()
    partners, query, status, date_from, date_to = _partner_queryset(request)
    paginator = Paginator(partners, 40)
    page_obj = paginator.get_page(request.GET.get('page'))
    page_numbers = page_obj.paginator.get_elided_page_range(
        page_obj.number, on_each_side=1, on_ends=1
    )
    params = request.GET.copy()
    params.pop('page', None)
    total_all = Partner.money_totals()
    total_filtered = Partner.money_totals(partners)
    filters_active = bool(query or status or date_from or date_to)
    return render(request, 'app/partners.html', _app_context(
        request,
        'Klijenti',
        page_obj=page_obj,
        page_numbers=page_numbers,
        query=query,
        status_filter=status,
        date_from=date_from.isoformat() if date_from else '',
        date_to=date_to.isoformat() if date_to else '',
        query_string=params.urlencode(),
        status_choices=Partner.STATUS_CHOICES,
        result_count=paginator.count,
        total_agreed_display=Partner.format_amount(total_all['agreed']),
        total_paid_display=Partner.format_amount(total_all['paid']),
        total_owed_display=Partner.format_amount(total_all['owed']),
        filtered_agreed_display=Partner.format_amount(total_filtered['agreed']),
        filtered_paid_display=Partner.format_amount(total_filtered['paid']),
        filtered_owed_display=Partner.format_amount(total_filtered['owed']),
        filters_active=filters_active,
    ))


def _save_partner(request, instance=None):
    partner = instance
    form = PartnerForm(request.POST or None, instance=partner)
    formset = PartnerPaymentFormSet(
        request.POST or None,
        instance=partner or Partner(),
        prefix='payments',
    )
    if request.method == 'POST' and form.is_valid() and formset.is_valid():
        partner = form.save()
        formset.instance = partner
        formset.save()
        partner.sync_amount()
        partner.apply_overdue()
        toast = 'saved' if instance else 'created'
        url = reverse('app_partner_detail', kwargs={'pk': partner.pk})
        return redirect(f'{url}?toast={toast}')
    return form, formset


@owner_required
def app_partner_create(request):
    saved = _save_partner(request)
    if not isinstance(saved, tuple):
        return saved
    form, formset = saved
    return render(request, 'app/partner_form.html', _app_context(
        request,
        'Novi unos',
        form=form,
        formset=formset,
        is_create=True,
    ))


@owner_required
def app_partner_detail(request, pk):
    Partner.mark_overdue()
    partner = get_object_or_404(Partner.objects.prefetch_related('payments'), pk=pk)
    return render(request, 'app/partner_detail.html', _app_context(
        request,
        partner.name,
        partner=partner,
    ))


@owner_required
def app_partner_edit(request, pk):
    partner = get_object_or_404(Partner, pk=pk)
    saved = _save_partner(request, partner)
    if not isinstance(saved, tuple):
        return saved
    form, formset = saved
    return render(request, 'app/partner_form.html', _app_context(
        request,
        f'Izmena — {partner.name}',
        form=form,
        formset=formset,
        partner=partner,
        is_create=False,
    ))


@owner_required
@require_POST
def app_partner_delete(request, pk):
    partner = get_object_or_404(Partner, pk=pk)
    partner.delete()
    return redirect(f"{reverse('app_partners')}?toast=deleted")
