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
        default='סדנה נשית\nחוויתית ומקצועית לגיל 40 +\nמותאמת לעולם הארגוני',
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

    # Editable images only (admin); text/overlay stay in code
    section2_image = models.ImageField(upload_to='homepage/section2/', blank=True, null=True)
    section3_image_1 = models.ImageField(upload_to='homepage/section3/', blank=True, null=True)
    section3_image_2 = models.ImageField(upload_to='homepage/section3/', blank=True, null=True)
    section3_image_3 = models.ImageField(upload_to='homepage/section3/', blank=True, null=True)
    section3_image_4 = models.ImageField(upload_to='homepage/section3/', blank=True, null=True)
    section4_image = models.ImageField(upload_to='homepage/section4/', blank=True, null=True)
    facilitators_image = models.ImageField(upload_to='homepage/facilitators/', blank=True, null=True)

    class Meta:
        verbose_name = 'דף בית'
        verbose_name_plural = 'דף בית'

    @classmethod
    def get_singleton(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return 'דף בית'


class HomePageQuote(models.Model):
    """ציטוט לסקשן 6 (קרוסלת משפטים)."""
    text = models.TextField(verbose_name='משפט')
    order = models.PositiveSmallIntegerField(default=0, verbose_name='סדר')

    class Meta:
        ordering = ['order', 'pk']
        verbose_name = 'ציטוט (סקשן 6)'
        verbose_name_plural = 'ציטוטים (סקשן 6)'

    def __str__(self):
        return (self.text[:50] + '…') if len(self.text) > 50 else self.text
