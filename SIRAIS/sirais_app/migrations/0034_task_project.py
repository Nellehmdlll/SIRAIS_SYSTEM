# Generated by Django 4.2.4 on 2023-10-27 08:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sirais_app', '0033_remove_task_assigned_to_remove_task_coach_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='sirais_app.project'),
        ),
    ]