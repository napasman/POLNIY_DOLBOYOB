# Generated by Django 3.2 on 2022-07-19 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_apiuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apiuser',
            name='balance',
            field=models.IntegerField(),
        ),
    ]
