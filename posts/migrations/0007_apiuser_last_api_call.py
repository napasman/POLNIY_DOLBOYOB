# Generated by Django 3.2 on 2022-07-19 22:19

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_apiuser_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='apiuser',
            name='last_api_call',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 19, 22, 19, 0, 86864, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
