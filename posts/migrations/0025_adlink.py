# Generated by Django 3.2 on 2023-09-10 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0024_referrallink'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.URLField()),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=100)),
                ('members', models.CharField(max_length=100)),
            ],
        ),
    ]
