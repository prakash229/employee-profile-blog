# Generated by Django 2.0.7 on 2018-08-10 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0003_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='picture',
            field=models.ImageField(blank=True, max_length=255, null=True, upload_to='media/pictures/%Y/%m/%d/'),
        ),
    ]
