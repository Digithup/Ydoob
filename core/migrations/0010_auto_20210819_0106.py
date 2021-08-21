# Generated by Django 3.1.7 on 2021-08-18 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20210819_0049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banners',
            name='position',
            field=models.CharField(choices=[('Top Left', 'Top Left'), ('Top Middle', 'Top Middle'), ('Top Right', 'Top Right'), ('Middle Left', 'Middle Left'), ('Middle Right', 'Middle Right'), ('Bottom Left', 'Bottom Left'), ('Bottom Middle', 'Bottom Middle'), ('Bottom Right', 'Bottom Right'), ('Collection Sidebar', 'Collection Sidebar')], max_length=150, unique=True),
        ),
    ]