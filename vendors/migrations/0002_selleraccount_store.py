# Generated by Django 3.1.4 on 2021-01-04 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='selleraccount',
            name='store',
            field=models.BooleanField(default=True),
        ),
    ]
