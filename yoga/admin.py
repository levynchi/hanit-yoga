from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.html import format_html
from .models import SiteSettings, HomePage, HomePageQuote


# SiteSettings: not in admin – header/logo edited in code only.
try:
    admin.site.unregister(SiteSettings)
except Exception:
    pass


@admin.register(HomePage)
class HomePageAdmin(admin.ModelAdmin):
    list_display = ('id', 'hero_image_preview_admin',)

    def changelist_view(self, request, extra_context=None):
        """Redirect /admin/yoga/homepage/ directly to the singleton's change form."""
        obj, _ = HomePage.objects.get_or_create(pk=1)
        return redirect(reverse('admin:yoga_homepage_change', args=[obj.pk]))
    readonly_fields = (
        'hero_image_preview',
        'section2_image_preview',
        'section3_image_1_preview',
        'section3_image_2_preview',
        'section3_image_3_preview',
        'section3_image_4_preview',
        'section4_image_preview',
        'facilitators_image_preview',
    )
    fieldsets = (
        ('באנר ראשי', {
            'fields': ('hero_image', 'hero_image_preview'),
        }),
        ('תמונת סקשן "למה זה חשוב דווקא עכשיו"', {
            'fields': ('section2_image', 'section2_image_preview'),
        }),
        ('ארבע תמונות – סביבת עבודה בריאה / השפעה ארגונית', {
            'fields': (
                ('section3_image_1', 'section3_image_1_preview'),
                ('section3_image_2', 'section3_image_2_preview'),
                ('section3_image_3', 'section3_image_3_preview'),
                ('section3_image_4', 'section3_image_4_preview'),
            ),
        }),
        ('תמונת סקשן "למה זה חשוב לנשים"', {
            'fields': ('section4_image', 'section4_image_preview'),
        }),
        ('תמונת המנחות', {
            'fields': ('facilitators_image', 'facilitators_image_preview'),
        }),
    )

    def _img_preview(self, url, max_h=80, max_w=160):
        if not url:
            return '-'
        return format_html(
            '<img src="{}" style="max-height: {}px; max-width: {}px; object-fit: cover;" />',
            url, max_h, max_w,
        )

    def _preview_url(self, field_file, static_path):
        """URL for preview: uploaded file or static fallback (what the site shows now)."""
        if field_file:
            return field_file.url
        if static_path:
            try:
                return staticfiles_storage.url(static_path)
            except Exception:
                pass
        return None

    def hero_image_preview_admin(self, obj):
        url = self._preview_url(obj.hero_image, 'yoga/images/hero-banner.png')
        return self._img_preview(url) or '-'

    hero_image_preview_admin.short_description = 'תמונת באנר'

    def hero_image_preview(self, obj):
        url = self._preview_url(obj.hero_image, 'yoga/images/hero-banner.png')
        return self._img_preview(url)

    hero_image_preview.short_description = 'תצוגה (מה שמוצג כרגע באתר)'

    def section2_image_preview(self, obj):
        url = self._preview_url(obj.section2_image, 'yoga/images/pic-section2.png')
        return self._img_preview(url)

    section2_image_preview.short_description = 'תצוגה (מה שמוצג כרגע באתר)'

    def section3_image_1_preview(self, obj):
        url = self._preview_url(obj.section3_image_1, 'yoga/images/ellipse4.png')
        return self._img_preview(url)

    section3_image_1_preview.short_description = 'תצוגה (מה שמוצג כרגע באתר)'

    def section3_image_2_preview(self, obj):
        url = self._preview_url(obj.section3_image_2, 'yoga/images/ellipse1.png')
        return self._img_preview(url)

    section3_image_2_preview.short_description = 'תצוגה (מה שמוצג כרגע באתר)'

    def section3_image_3_preview(self, obj):
        url = self._preview_url(obj.section3_image_3, 'yoga/images/ellipse2.png')
        return self._img_preview(url)

    section3_image_3_preview.short_description = 'תצוגה (מה שמוצג כרגע באתר)'

    def section3_image_4_preview(self, obj):
        url = self._preview_url(obj.section3_image_4, 'yoga/images/ellipse3.png')
        return self._img_preview(url)

    section3_image_4_preview.short_description = 'תצוגה (מה שמוצג כרגע באתר)'

    def section4_image_preview(self, obj):
        url = self._preview_url(obj.section4_image, 'yoga/images/pic-section4.png')
        return self._img_preview(url)

    section4_image_preview.short_description = 'תצוגה (מה שמוצג כרגע באתר)'

    def facilitators_image_preview(self, obj):
        url = self._preview_url(obj.facilitators_image, 'yoga/images/facilitators.png')
        return self._img_preview(url)

    facilitators_image_preview.short_description = 'תצוגה (מה שמוצג כרגע באתר)'


@admin.register(HomePageQuote)
class HomePageQuoteAdmin(admin.ModelAdmin):
    list_display = ('order', 'text_short', 'id')
    list_display_links = ('text_short',)
    list_editable = ('order',)
    ordering = ('order', 'pk')

    def text_short(self, obj):
        return (obj.text[:60] + '…') if len(obj.text) > 60 else obj.text
    text_short.short_description = 'משפט'
