# Generated by Django 3.2.6 on 2021-09-08 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0002_notification_extra_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(choices=[('message', 'Message'), ('application', 'Application'), ('new_order', 'NewOrder')], max_length=20),
        ),
    ]