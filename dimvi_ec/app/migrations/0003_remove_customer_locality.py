# Generated by Django 4.2.13 on 2024-06-10 19:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_customer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='locality',
        ),
    ]
