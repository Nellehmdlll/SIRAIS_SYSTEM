# Generated by Django 4.2.4 on 2023-09-06 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sirais_app', '0017_alter_customuser_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='address',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
