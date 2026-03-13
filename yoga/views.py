from pathlib import Path
from django.conf import settings as django_settings
from django.shortcuts import render
from .constants import SECTION7_DEFAULT_TEXTS
from .models import SiteSettings, HomePage, HomePageQuote, Section7Testimonial


def _static_images_dir():
    return Path(django_settings.BASE_DIR) / "yoga" / "static" / "yoga" / "images"


def _find_hero_banner(img_dir):
    # Prefer PNG (Figma export = HERO BANNER MOBILE 210:41580), then jpg, webp
    for ext in ("png", "jpg", "webp"):
        path = img_dir / f"hero-banner.{ext}"
        if path.exists():
            return f"yoga/images/hero-banner.{ext}"
    return None


def home(request):
    site_settings = SiteSettings.get_singleton()
    homepage = HomePage.get_singleton()
    img_dir = _static_images_dir()
    has_logo_png = (img_dir / "logo.png").exists()
    has_header_png = (img_dir / "header.png").exists()
    hero_banner_file = _find_hero_banner(img_dir)
    quotes = list(HomePageQuote.objects.all())
    testimonials_by_order = {obj.order: obj for obj in Section7Testimonial.objects.all()}
    section7_card_classes = ['pink-light', 'teal', 'white', 'pink', 'border', 'teal']
    section7_icons = [
        'yoga/images/icon-quotes-pink.svg',
        'yoga/images/icon-quotes-teal.svg',
        'yoga/images/icon-quotes-pink.svg',
        'yoga/images/icon-quotes-pink.svg',
        'yoga/images/icon-quotes-dark.svg',
        'yoga/images/icon-quotes-teal.svg',
    ]
    section7_texts = []
    for i in range(6):
        obj = testimonials_by_order.get(i + 1)
        if obj and obj.text and obj.text.strip():
            section7_texts.append(obj.text.strip())
        else:
            section7_texts.append(SECTION7_DEFAULT_TEXTS[i])
    section7_cards = [
        {'text': section7_texts[i], 'card_class': section7_card_classes[i], 'icon': section7_icons[i]}
        for i in range(6)
    ]
    context = {
        "site_settings": site_settings,
        "homepage": homepage,
        "section6_quotes": quotes,
        "section7_cards": section7_cards,
        "use_figma_logo": has_logo_png or has_header_png,
        "figma_logo_file": "yoga/images/logo.png" if has_logo_png else "yoga/images/header.png" if has_header_png else None,
        "figma_logo_crop": has_header_png and not has_logo_png,
        "use_figma_hero": hero_banner_file is not None,
        "figma_hero_file": hero_banner_file,
    }
    return render(request, "yoga/home.html", context)
