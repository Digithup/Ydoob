# Generated by Django 3.1.7 on 2021-08-21 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_wishlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='is_featured',
            field=models.BooleanField(default=False),
        ),
    ]
