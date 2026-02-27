from django.db import models


class SiteSettings(models.Model):
    """Singleton: logo, logo text image, header tagline."""
    logo = models.ImageField(upload_to='site/', blank=True, null=True)
    logo_text = models.ImageField(
        upload_to='site/',
        blank=True,
        null=True,
        help_text='Logo text image (תבונת המעבר)',
    )
    header_tagline = models.CharField(
        max_length=300,
        default='מרחב לנשים באמצע החיים',
    )

    class Meta:
        verbose_name = 'הגדרות אתר'
        verbose_name_plural = 'הגדרות אתר'

    @classmethod
    def get_singleton(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return 'הגדרות אתר'


class HomePage(models.Model):
    """Singleton: hero section content."""
    hero_image = models.ImageField(upload_to='hero/', blank=True, null=True)
    hero_overlay_title = models.CharField(
        max_length=200,
        default='"אם היית פרח"',
    )
    hero_overlay_text = models.TextField(
        default='סדנה נשית חוויתית ומקצועית ומותאמת לעולם הארגוני',
    )
    hero_overlay_image = models.ImageField(
        upload_to='hero/',
        blank=True,
        null=True,
        help_text='Flower image',
    )
    hero_subtitle = models.CharField(
        max_length=300,
        default='הסדנה מיועדת לנשים בגיל 40+',
    )
    hero_cta_text = models.CharField(
        max_length=100,
        default='לתיאום סדנאות',
    )
    hero_cta_link = models.URLField(blank=True, default='#contact')

    class Meta:
        verbose_name = 'דף בית'
        verbose_name_plural = 'דף בית'

    @classmethod
    def get_singleton(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return 'דף בית'
