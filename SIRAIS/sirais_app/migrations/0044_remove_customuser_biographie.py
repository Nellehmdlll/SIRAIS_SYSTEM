# Generated by Django 4.2.4 on 2023-10-29 12:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sirais_app', '0043_alter_customuser_biographie'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='biographie',
        ),
    ]
