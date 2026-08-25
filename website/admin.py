from django.contrib import admin
from django.utils.html import format_html
from .images import ImageProcessingError, normalize_cover
from .models import Article, ArticleImage, ContactMessage, Partner, PartnerPayment
from .translate import fill_empty_translations


class ArticleImageInline(admin.TabularInline):
    model = ArticleImage
    extra = 1
    fields = ('image', 'caption', 'sort_order')
    verbose_name = 'Dodatna slika'
    verbose_name_plural = 'Dodatne slike u vestima'


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published', 'published_at', 'cover_preview')
    list_filter = ('is_published',)
    list_editable = ('is_published',)
    search_fields = (
        'title', 'excerpt', 'body',
        'title_en', 'excerpt_en', 'body_en',
        'title_ru', 'excerpt_ru', 'body_ru',
    )
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'
    inlines = [ArticleImageInline]
    fieldsets = (
        ('Srpski', {
            'fields': ('title', 'excerpt', 'body'),
            'description': (
                'Obavezno. Prazan prevod na engleski i ruski popunjava se automatski pri čuvanju. '
                'Posle toga možete da korigujete tekst.'
            ),
        }),
        ('English', {
            'fields': ('title_en', 'excerpt_en', 'body_en'),
        }),
        ('Русский', {
            'fields': ('title_ru', 'excerpt_ru', 'body_ru'),
        }),
        ('Slika i objava', {
            'fields': ('cover', 'is_published', 'published_at', 'slug', 'header_image'),
        }),
    )

    class Media:
        js = (
            'https://cdn.jsdelivr.net/npm/tinymce@7.6.0/tinymce.min.js',
            'admin/js/tinymce_init.js',
        )

    def save_model(self, request, obj, form, change):
        if form.cleaned_data.get('cover') and 'cover' in form.changed_data:
            try:
                obj.cover = normalize_cover(form.cleaned_data['cover'])
            except ImageProcessingError:
                pass
        filled = fill_empty_translations(obj)
        super().save_model(request, obj, form, change)
        if filled:
            self.message_user(
                request,
                'Prevod na engleski i ruski je automatski popunjen. Proverite ga pre objave.',
            )

    def cover_preview(self, obj):
        if not obj.cover:
            return '—'
        return format_html(
            '<img src="{}" style="height:40px;width:auto;border-radius:2px;" />',
            obj.cover.url,
        )
    cover_preview.short_description = 'Slika'


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'created_at', 'is_read')
    list_filter = ('is_read',)
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('name', 'email', 'phone', 'message', 'created_at')


class PartnerPaymentInline(admin.TabularInline):
    model = PartnerPayment
    extra = 1


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'recorded_on', 'due_on', 'amount', 'status', 'updated_at')
    list_filter = ('status', 'recorded_on', 'due_on')
    search_fields = ('name', 'description')
    readonly_fields = ('amount',)
    inlines = [PartnerPaymentInline]

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        form.instance.sync_amount()
        form.instance.apply_overdue()
