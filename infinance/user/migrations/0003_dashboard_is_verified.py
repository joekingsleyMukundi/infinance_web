# Generated by Django 4.0 on 2021-12-20 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_dashboard_otp'),
    ]

    operations = [
        migrations.AddField(
            model_name='dashboard',
            name='is_verified',
            field=models.IntegerField(default=False),
        ),
    ]
