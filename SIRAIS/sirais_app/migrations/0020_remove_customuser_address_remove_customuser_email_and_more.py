# Generated by Django 4.2.4 on 2023-09-06 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sirais_app', '0019_alter_customuser_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='address',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='email',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='expertise',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='photo',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='phone',
            field=models.CharField(default='345656', max_length=100),
        ),
    ]
