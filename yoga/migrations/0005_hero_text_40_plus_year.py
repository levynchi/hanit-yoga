# Generated manually

from django.db import migrations


def update_40_plus(apps, schema_editor):
    HomePage = apps.get_model('yoga', 'HomePage')
    for obj in HomePage.objects.all():
        if '40 פלוס' in obj.hero_overlay_text:
            obj.hero_overlay_text = obj.hero_overlay_text.replace('40 פלוס', '40 + שנה')
            obj.save()


def reverse_40_plus(apps, schema_editor):
    HomePage = apps.get_model('yoga', 'HomePage')
    for obj in HomePage.objects.all():
        if '40 + שנה' in obj.hero_overlay_text:
            obj.hero_overlay_text = obj.hero_overlay_text.replace('40 + שנה', '40 פלוס')
            obj.save()


class Migration(migrations.Migration):

    dependencies = [
        ('yoga', '0004_hero_overlay_text_line_breaks'),
    ]

    operations = [
        migrations.RunPython(update_40_plus, reverse_40_plus),
    ]
