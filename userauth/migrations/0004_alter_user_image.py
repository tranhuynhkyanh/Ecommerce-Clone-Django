# Generated by Django 3.2.1 on 2023-10-17 10:17

from django.db import migrations, models
import userauth.models


class Migration(migrations.Migration):

    dependencies = [
        ('userauth', '0003_user_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(default='none.jpg', null=True, upload_to=userauth.models.user_directory_path),
        ),
    ]