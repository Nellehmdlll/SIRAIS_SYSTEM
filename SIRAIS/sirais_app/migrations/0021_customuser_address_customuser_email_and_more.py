# Generated by Django 4.2.4 on 2023-09-07 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sirais_app', '0020_remove_customuser_address_remove_customuser_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='address',
            field=models.CharField(default=None, max_length=200),
        ),
        migrations.AddField(
            model_name='customuser',
            name='email',
            field=models.EmailField(default=None, max_length=254),
        ),
        migrations.AddField(
            model_name='customuser',
            name='expertise',
            field=models.CharField(default=None, max_length=200),
        ),
    ]