# Generated by Django 3.1.7 on 2021-07-29 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_auto_20210729_2222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='filter',
            field=models.ManyToManyField(blank=True, null=True, related_name='product_filter', to='catalog.Filters'),
        ),
        migrations.AlterField(
            model_name='products',
            name='manufacturer',
            field=models.ManyToManyField(blank=True, null=True, related_name='product_manufacturer', to='catalog.Manufacturer'),
        ),
        migrations.AlterField(
            model_name='products',
            name='related',
            field=models.ManyToManyField(blank=True, null=True, related_name='_products_related_+', to='catalog.Products'),
        ),
    ]
