# Generated by Django 3.2 on 2023-06-06 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0016_auto_20220807_1920'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='heading_image',
            field=models.ImageField(blank=True, default='profile_pictures/images_3.jpg', upload_to=''),
        ),
    ]
