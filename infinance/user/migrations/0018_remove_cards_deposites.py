# Generated by Django 4.0 on 2021-12-29 11:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0017_cards_deposites'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cards',
            name='deposites',
        ),
    ]
