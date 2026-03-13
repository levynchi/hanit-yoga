# Remove "שנה" from hero overlay text (e.g. "40 + שנה" -> "40 +")

from django.db import migrations


def remove_year(apps, schema_editor):
    HomePage = apps.get_model('yoga', 'HomePage')
    for obj in HomePage.objects.all():
        if '40 + שנה' in obj.hero_overlay_text:
            obj.hero_overlay_text = obj.hero_overlay_text.replace('40 + שנה', '40 +')
            obj.save()


def add_year_back(apps, schema_editor):
    HomePage = apps.get_model('yoga', 'HomePage')
    for obj in HomePage.objects.all():
        if '40 +' in obj.hero_overlay_text and 'שנה' not in obj.hero_overlay_text:
            obj.hero_overlay_text = obj.hero_overlay_text.replace('40 +', '40 + שנה', 1)
            obj.save()


class Migration(migrations.Migration):

    dependencies = [
        ('yoga', '0005_hero_text_40_plus_year'),
    ]

    operations = [
        migrations.RunPython(remove_year, add_year_back),
    ]
