# Generated by Django 3.1.7 on 2021-07-08 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0011_auto_20210708_1327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='email',
            field=models.EmailField(max_length=50, null=True, unique=True, verbose_name='Store Email'),
        ),
    ]
