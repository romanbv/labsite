# Generated by Django 4.1.7 on 2023-04-01 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.TextField(blank=True, max_length=500, null=True, verbose_name='Название'),
        ),
    ]
