# Generated by Django 3.2 on 2022-08-07 17:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0014_auto_20220807_1909'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apiuser',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='api_user', to=settings.AUTH_USER_MODEL, unique=True),
        ),
    ]
