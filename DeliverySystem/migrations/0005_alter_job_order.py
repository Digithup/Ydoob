# Generated by Django 3.2.6 on 2021-09-12 21:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0006_alter_orderproduct_delivery_by'),
        ('DeliverySystem', '0004_auto_20210912_2342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='order',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sales.order'),
        ),
    ]