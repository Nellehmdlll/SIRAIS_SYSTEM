# Generated by Django 4.2.4 on 2023-10-29 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sirais_app', '0039_alter_customuser_biographie'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='biographie',
            field=models.TextField(blank=True, default='Votre adresse par défaut', max_length=1200),
        ),
    ]