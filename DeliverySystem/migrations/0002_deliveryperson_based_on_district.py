# Generated by Django 3.2.6 on 2021-09-06 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('DeliverySystem', '0001_initial'),
        ('sales', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliveryperson',
            name='based_on_district',
            field=models.ManyToManyField(blank=True, related_name='delivery_district', to='sales.Location'),
        ),
    ]
