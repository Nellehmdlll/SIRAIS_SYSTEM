# Generated by Django 4.2.4 on 2023-08-20 01:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sirais_app', '0003_remove_resource_description_remove_resource_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='title',
            field=models.CharField(default='Entrez un titre', max_length=200),
        ),
    ]
