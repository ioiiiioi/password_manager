# Generated by Django 4.1.7 on 2023-03-05 10:21

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('is_active', models.BooleanField(default=False)),
                ('is_sandbox', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('private_metadata', models.JSONField(default=dict)),
                ('public_metadata', models.JSONField(default=dict)),
                ('plan', models.CharField(choices=[('FREE', 'FREE'), ('PREMIUM', 'PREMIUM'), ('CUSTOM', 'CUSTOM')], default='FREE', max_length=7)),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('is_active', models.BooleanField(default=False)),
                ('is_sandbox', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('private_metadata', models.JSONField(default=dict)),
                ('public_metadata', models.JSONField(default=dict)),
                ('name', models.CharField(max_length=50)),
                ('alias', models.CharField(max_length=25)),
                ('address', models.TextField(blank=True, null=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('plan', models.CharField(choices=[('FREE', 'FREE'), ('PREMIUM', 'PREMIUM'), ('CUSTOM', 'CUSTOM')], default='FREE', max_length=7)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='organization_created_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('is_active', models.BooleanField(default=False)),
                ('is_sandbox', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(max_length=50)),
                ('type', models.CharField(choices=[('ORGANIZATION', 'ORGANIZATION'), ('PERSONAL', 'PERSONAL'), ('TEAM', 'TEAM')], max_length=13)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teams_creator', to=settings.AUTH_USER_MODEL)),
                ('member', models.ManyToManyField(blank=True, related_name='teams', to=settings.AUTH_USER_MODEL)),
                ('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='teams', to='core.organization')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='user',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users', to='core.organization'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]
