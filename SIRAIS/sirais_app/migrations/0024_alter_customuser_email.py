# Generated by Django 4.2.4 on 2023-09-10 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sirais_app', '0023_customuser_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(blank=True, default=None, max_length=254),
        ),
    ]