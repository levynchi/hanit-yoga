# Data migration: create 6 empty Section7Testimonial slots (order 1–6) so admin can edit them; site shows defaults until filled.

from django.db import migrations


def create_section7_slots(apps, schema_editor):
    Section7Testimonial = apps.get_model('yoga', 'Section7Testimonial')
    for order in range(1, 7):
        Section7Testimonial.objects.get_or_create(order=order, defaults={'text': ''})


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('yoga', '0007_section7_testimonials'),
    ]

    operations = [
        migrations.RunPython(create_section7_slots, noop_reverse),
    ]
