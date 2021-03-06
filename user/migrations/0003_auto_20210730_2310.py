# Generated by Django 3.2.2 on 2021-07-30 20:10

from django.db import migrations
import imagekit.models.fields
import user.utils


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20210730_2244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=imagekit.models.fields.ProcessedImageField(null=True, upload_to=user.utils.upload_to_user_directory),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='cover',
            field=imagekit.models.fields.ProcessedImageField(null=True, upload_to=user.utils.upload_to_user_directory),
        ),
    ]
