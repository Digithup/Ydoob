# Generated by Django 3.1.4 on 2020-12-25 13:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_auto_20201225_1620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='album',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='model', to='catalog.imagealbum'),
        ),
    ]
