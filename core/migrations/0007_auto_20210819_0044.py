# Generated by Django 3.1.7 on 2021-08-18 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20210819_0035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banners',
            name='position',
            field=models.CharField(choices=[('Top Left', 'Top Left'), ('2', 'Top Middle'), ('3', 'Top Right'), ('4', 'Middle Left'), ('5', 'Middle Right'), ('6', 'Bottom Left'), ('7', 'Bottom Middle'), ('7', 'Bottom Right')], max_length=150, unique=True),
        ),
    ]