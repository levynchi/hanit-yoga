# Generated manually

from django.db import migrations


def update_hero_text(apps, schema_editor):
    HomePage = apps.get_model('yoga', 'HomePage')
    new_text = 'סדנה נשית\nחוויתית ומקצועית לגיל 40 פלוס\nמותאמת לעולם הארגוני'
    # Update all HomePage records that still have the old single-line default
    old_text = 'סדנה נשית חוויתית ומקצועית ומותאמת לעולם הארגוני'
    HomePage.objects.filter(hero_overlay_text=old_text).update(hero_overlay_text=new_text)


def reverse_hero_text(apps, schema_editor):
    HomePage = apps.get_model('yoga', 'HomePage')
    old_text = 'סדנה נשית חוויתית ומקצועית ומותאמת לעולם הארגוני'
    new_text = 'סדנה נשית\nחוויתית ומקצועית לגיל 40 פלוס\nמותאמת לעולם הארגוני'
    HomePage.objects.filter(hero_overlay_text=new_text).update(hero_overlay_text=old_text)


class Migration(migrations.Migration):

    dependencies = [
        ('yoga', '0003_section6_quotes'),
    ]

    operations = [
        migrations.RunPython(update_hero_text, reverse_hero_text),
    ]
