# Generated by Django 4.2.4 on 2023-09-07 11:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sirais_app', '0021_customuser_address_customuser_email_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='address',
        ),
    ]
