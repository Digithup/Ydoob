# Generated by Django 3.2.6 on 2021-09-22 01:43

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Courier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lat', models.FloatField(default=0)),
                ('lng', models.FloatField(default=0)),
                ('paypal_email', models.EmailField(blank=True, max_length=255)),
                ('fcm_token', models.TextField(blank=True)),
                ('status', models.CharField(choices=[('True', 'Yes'), ('False', 'NO')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Shipping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('creating', 'Creating'), ('processing', 'Processing'), ('picking', 'Picking'), ('delivering', 'Delivering'), ('completed', 'Completed'), ('canceled', 'Canceled')], default='creating', max_length=255)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('vendor_lat', models.FloatField(default=0)),
                ('vendor_lng', models.FloatField(default=0)),
                ('customer_lat', models.FloatField(default=0)),
                ('customer_lng', models.FloatField(default=0)),
                ('duration', models.IntegerField(default=0)),
                ('distance', models.FloatField(default=0)),
                ('price', models.FloatField(default=0)),
                ('pickup_photo', models.ImageField(blank=True, null=True, upload_to='job/pickup_photos/')),
                ('pickup_at', models.DateTimeField(blank=True, null=True)),
                ('delivery_photo', models.ImageField(blank=True, null=True, upload_to='job/delivery_photos/')),
                ('delivered_at', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=255, null=True)),
                ('amount', models.FloatField(default=0)),
                ('status', models.CharField(choices=[('in', 'In'), ('out', 'Out')], default='in', max_length=20)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('shipping', models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='DeliverySystem.shipping')),
            ],
        ),
    ]
