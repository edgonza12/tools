# Generated by Django 5.2.1 on 2025-05-21 21:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_module_usermodulepermission'),
    ]

    operations = [
        migrations.AddField(
            model_name='module',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='submodules', to='accounts.module'),
        ),
        migrations.AlterField(
            model_name='module',
            name='icon',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='module',
            name='url_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
