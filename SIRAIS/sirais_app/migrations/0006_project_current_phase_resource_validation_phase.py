# Generated by Django 4.2.4 on 2023-08-21 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sirais_app', '0005_resource_desc_alter_resource_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='current_phase',
            field=models.CharField(choices=[('ideation', 'Idéation'), ('prototypage', 'Prototypage'), ('modele_economique', 'Modèle économique'), ('entree_marche', 'Entrée sur le marché')], default='ideation', max_length=20),
        ),
        migrations.AddField(
            model_name='resource',
            name='validation_phase',
            field=models.CharField(blank=True, choices=[('ideation', 'Idéation'), ('prototypage', 'Prototypage'), ('modele_economique', 'Modèle économique'), ('entree_marche', 'Entrée sur le marché')], max_length=20),
        ),
    ]
