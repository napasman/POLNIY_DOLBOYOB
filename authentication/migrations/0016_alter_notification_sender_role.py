# Generated by Django 3.2 on 2023-10-25 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0015_auto_20231025_2051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='sender_role',
            field=models.CharField(choices=[('Administrator', 'Administrator'), ('Leader', 'Leader')], max_length=20),
        ),
    ]
