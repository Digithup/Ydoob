# Generated by Django 3.1.7 on 2021-07-14 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0012_auto_20210714_1543'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='requires_shipping',
            field=models.CharField(choices=[('True', 'Yes'), ('False', 'NO')], default=False, max_length=65, null=True),
        ),
    ]
