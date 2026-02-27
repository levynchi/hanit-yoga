from pathlib import Path
from django.conf import settings as django_settings
from django.shortcuts import render
from .models import SiteSettings, HomePage


def _static_images_dir():
    return Path(django_settings.BASE_DIR) / "yoga" / "static" / "yoga" / "images"


def _find_hero_banner(img_dir):
    for ext in ("jpg", "png", "webp"):
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
    context = {
        "site_settings": site_settings,
        "homepage": homepage,
        "use_figma_logo": has_logo_png or has_header_png,
        "figma_logo_file": "yoga/images/logo.png" if has_logo_png else "yoga/images/header.png" if has_header_png else None,
        "figma_logo_crop": has_header_png and not has_logo_png,
        "use_figma_hero": hero_banner_file is not None,
        "figma_hero_file": hero_banner_file,
    }
    return render(request, "yoga/home.html", context)
