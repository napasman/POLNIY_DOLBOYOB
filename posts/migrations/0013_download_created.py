# Generated by Django 3.2 on 2022-08-01 21:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0012_rename_downlaods_apiuser_downloads'),
    ]

    operations = [
        migrations.AddField(
            model_name='download',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
