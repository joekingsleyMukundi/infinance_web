# Generated by Django 4.0 on 2021-12-29 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0014_cards_is_deleted'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactions',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]