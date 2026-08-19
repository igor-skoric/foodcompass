from django.contrib import admin
from django.utils.html import format_html
from .models import Article, ArticleImage, ContactMessage, Partner


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
    search_fields = ('title', 'excerpt', 'body')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'
    inlines = [ArticleImageInline]
    fieldsets = (
        ('Vest', {
            'fields': ('title', 'excerpt', 'cover', 'body'),
            'description': 'Naslov, kratak opis i slika idu na listu Aktuelnosti. Tekst se prikazuje na stranici vesti.',
        }),
        ('Objava', {
            'fields': ('is_published', 'published_at', 'slug'),
        }),
        ('Header slika', {
            'classes': ('collapse',),
            'fields': ('header_image',),
            'description': 'Opciono. Ako je prazno, u headeru vesti koristi se slika iznad.',
        }),
    )

    class Media:
        js = (
            'https://cdn.jsdelivr.net/npm/tinymce@7.6.0/tinymce.min.js',
            'admin/js/tinymce_init.js',
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


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'recorded_on', 'amount', 'status', 'updated_at')
    list_filter = ('status', 'recorded_on')
    search_fields = ('name', 'description')
