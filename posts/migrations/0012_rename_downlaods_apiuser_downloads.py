# Generated by Django 3.2 on 2022-08-01 09:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0011_auto_20220801_1141'),
    ]

    operations = [
        migrations.RenameField(
            model_name='apiuser',
            old_name='downlaods',
            new_name='downloads',
        ),
    ]
