from django.contrib import admin
from django.utils.html import format_html
from .models import SiteSettings, HomePage


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'logo_preview', 'header_tagline_short')
    readonly_fields = ('logo_preview', 'logo_text_preview')

    def logo_preview(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" style="max-height: 60px; max-width: 120px;" />',
                obj.logo.url,
            )
        return '-'

    logo_preview.short_description = 'לוגו'

    def logo_text_preview(self, obj):
        if obj.logo_text:
            return format_html(
                '<img src="{}" style="max-height: 40px; max-width: 200px;" />',
                obj.logo_text.url,
            )
        return '-'

    logo_text_preview.short_description = 'תמונת טקסט לוגו'

    def header_tagline_short(self, obj):
        return (obj.header_tagline or '')[:50] + ('…' if len(obj.header_tagline or '') > 50 else '')

    header_tagline_short.short_description = 'טקסט הדר'


@admin.register(HomePage)
class HomePageAdmin(admin.ModelAdmin):
    list_display = ('id', 'hero_image_preview', 'hero_overlay_title_short', 'hero_cta_text')
    readonly_fields = ('hero_image_preview', 'hero_overlay_image_preview')

    def hero_image_preview(self, obj):
        if obj.hero_image:
            return format_html(
                '<img src="{}" style="max-height: 80px; max-width: 160px; object-fit: cover;" />',
                obj.hero_image.url,
            )
        return '-'

    hero_image_preview.short_description = 'תמונת באנר'

    def hero_overlay_image_preview(self, obj):
        if obj.hero_overlay_image:
            return format_html(
                '<img src="{}" style="max-height: 60px; max-width: 120px;" />',
                obj.hero_overlay_image.url,
            )
        return '-'

    hero_overlay_image_preview.short_description = 'תמונת פרח'

    def hero_overlay_title_short(self, obj):
        return (obj.hero_overlay_title or '')[:30] + ('…' if len(obj.hero_overlay_title or '') > 30 else '')

    hero_overlay_title_short.short_description = 'כותרת באנר'
