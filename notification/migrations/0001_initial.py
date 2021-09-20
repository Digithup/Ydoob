# Generated by Django 3.2.6 on 2021-09-20 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_type', models.CharField(choices=[('message', 'Message'), ('application', 'Application'), ('new_order', 'NewOrder'), ('NewRegistration', 'NewRegistration'), ('NewVendorCreate', 'NewVendorCreate')], max_length=20)),
                ('is_read', models.BooleanField(default=False)),
                ('extra_id', models.IntegerField(blank=True, null=True)),
                ('extra_info', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
