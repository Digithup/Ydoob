# Generated by Django 3.2.6 on 2021-09-08 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='extra_info',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]