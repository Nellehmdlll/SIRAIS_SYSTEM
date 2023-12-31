# Generated by Django 4.2.3 on 2023-08-08 12:02

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_type', models.CharField(choices=[('coach', 'Coach'), ('mentor', 'Mentor'), ('project_owner', 'Porteur de projet')], default='coach', max_length=50)),
                ('expertise', models.CharField(blank=True, max_length=200)),
                ('experience', models.IntegerField(default=0)),
                ('photo', models.ImageField(blank=True, default='img/default_coach.jpg', upload_to='img_coachProfile', verbose_name='photo de profil')),
                ('company', models.CharField(blank=True, max_length=200)),
                ('mentor_expertise', models.CharField(blank=True, max_length=200)),
                ('bio', models.TextField(blank=True)),
                ('mentor_photo', models.ImageField(blank=True, default='img/default_mentor.jpg', upload_to='img_mentorProfile', verbose_name='photo de profil')),
                ('phone_number', models.CharField(blank=True, max_length=20)),
                ('project_owner_photo', models.ImageField(blank=True, default='img/default_project_owner.jpg', upload_to='img_projectOwnerProfile', verbose_name='photo de profil')),
                ('groups', models.ManyToManyField(blank=True, related_name='users_group', to='auth.group')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('desc', models.TextField(blank=True)),
                ('start_date', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('end_date', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('state_date', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('project_state', models.CharField(blank=True, choices=[('in_progress', 'En cours'), ('completed', 'Terminé'), ('on_hold', 'En attente')], max_length=20)),
                ('coach', models.ForeignKey(default=None, limit_choices_to={'groups__name': 'Coaches'}, on_delete=django.db.models.deletion.CASCADE, related_name='projets_coach', to=settings.AUTH_USER_MODEL)),
                ('porteur_de_projet', models.ForeignKey(default=None, limit_choices_to={'groups__name': 'Porteurs de projet'}, on_delete=django.db.models.deletion.CASCADE, related_name='projets_porteur', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('progress', models.IntegerField(default=0)),
                ('start_date', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('due_date', models.DateTimeField(blank=True, null=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sirais_app.project')),
            ],
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('file', models.FileField(upload_to='resources/')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sirais_app.project')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectOwnerProjectAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assignment_date', models.DateTimeField(auto_now_add=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sirais_app.project')),
                ('project_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_owner_assignments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(limit_choices_to=models.Q(('coach__isnull', False), ('mentor__isnull', False), _connector='OR'), on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sirais_app.project')),
                ('task', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sirais_app.task')),
            ],
        ),
        migrations.CreateModel(
            name='CoachProjectAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assignment_date', models.DateTimeField(auto_now_add=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sirais_app.project')),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='coach_assignments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
