# Generated by Django 3.1.7 on 2021-07-15 12:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0016_auto_20210715_1359'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productmedia',
            options={'ordering': ['product'], 'verbose_name_plural': 'Product Image'},
        ),
        migrations.RenameField(
            model_name='productmedia',
            old_name='media_content',
            new_name='media',
        ),
    ]
