# Generated by Django 3.1.7 on 2021-08-21 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0008_auto_20210821_1342'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categories',
            name='title',
        ),
        migrations.AddField(
            model_name='categories',
            name='title_ar',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='categories',
            name='title_en',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]