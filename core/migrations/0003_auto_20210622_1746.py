# Generated by Django 3.1.7 on 2021-06-22 15:46

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_delete_images'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='settinglang',
            name='slug',
        ),
        migrations.AddField(
            model_name='setting',
            name='slug',
            field=models.SlugField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
