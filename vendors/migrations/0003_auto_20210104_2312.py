# Generated by Django 3.1.4 on 2021-01-04 20:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0002_selleraccount_store'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='selleraccount',
            name='active',
        ),
        migrations.RemoveField(
            model_name='selleraccount',
            name='managers',
        ),
        migrations.RemoveField(
            model_name='selleraccount',
            name='store',
        ),
        migrations.RemoveField(
            model_name='selleraccount',
            name='timestamp',
        ),
        migrations.RemoveField(
            model_name='selleraccount',
            name='user',
        ),
    ]
