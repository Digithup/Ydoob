# Generated by Django 3.1.4 on 2021-01-04 20:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_remove_manufacturer_store'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sellerproduct',
            name='seller',
        ),
    ]
