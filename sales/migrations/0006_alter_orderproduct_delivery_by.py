# Generated by Django 3.2.6 on 2021-09-12 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0005_alter_orderproduct_delivery_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproduct',
            name='delivery_by',
            field=models.CharField(choices=[('Ydoob', 'Ydoob'), ('Self', 'Self')], default=False, max_length=10),
        ),
    ]