# Generated by Django 3.1.4 on 2020-12-28 20:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_auto_20201228_2258'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='level',
        ),
        migrations.RemoveField(
            model_name='category',
            name='lft',
        ),
        migrations.RemoveField(
            model_name='category',
            name='rght',
        ),
        migrations.RemoveField(
            model_name='category',
            name='tree_id',
        ),
    ]
