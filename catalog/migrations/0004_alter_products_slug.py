# Generated by Django 3.2.6 on 2021-09-15 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_auto_20210915_2039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='slug',
            field=models.SlugField(blank=True, max_length=128, null=True, unique=True),
        ),
    ]
