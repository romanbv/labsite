# Generated by Django 3.2.14 on 2022-10-20 19:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.FileField(blank=True, null=True, upload_to='', verbose_name='Аватар')),
                ('bio', models.TextField(blank=True, max_length=500, null=True, verbose_name='О себе')),
                ('city', models.CharField(blank=True, max_length=30, null=True, verbose_name='Город')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='Дата рождения')),
                ('gender', models.CharField(choices=[['none', 'Не определенно'], ['male', 'Мужской'], ['female', 'Женский']], default='none', max_length=10, verbose_name='Пол')),
                ('profile_type', models.CharField(choices=[['none', 'Не определенно'], ['doctor', 'Врач'], ['tehnik', 'Техник']], default='none', max_length=20, verbose_name='Тип профиля')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
        ),
    ]
