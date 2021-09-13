# Generated by Django 3.2.6 on 2021-09-12 00:15

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('currencies', '0006_increase_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('first_name', models.CharField(blank=True, max_length=200, null=True)),
                ('last_name', models.CharField(blank=True, max_length=200, null=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('image', models.ImageField(default='images/dashboard-bases/man.png', upload_to='images/Users/%y/%m')),
                ('facebook', models.URLField(blank=True, max_length=50)),
                ('instagram', models.URLField(blank=True, max_length=50)),
                ('twitter', models.URLField(blank=True, max_length=50)),
                ('youtube', models.URLField(blank=True, max_length=50)),
                ('about', ckeditor_uploader.fields.RichTextUploadingField(blank=True)),
                ('active', models.BooleanField(default=True)),
                ('is_active', models.BooleanField(default=True)),
                ('customer', models.BooleanField(default=True)),
                ('seller', models.BooleanField(default=False)),
                ('staff', models.BooleanField(default=False)),
                ('admin', models.BooleanField(default=False)),
                ('slug', models.SlugField(unique=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('currency', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='currencies.currency')),
                ('groups', models.ManyToManyField(blank=True, to='auth.Group')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GuestEmail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('active', models.BooleanField(default=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Guest User',
                'verbose_name_plural': 'Guest Users',
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='UserAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_title', models.CharField(max_length=150)),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(blank=True, max_length=150, null=True)),
                ('governorate', models.CharField(blank=True, max_length=150, null=True)),
                ('city', models.CharField(blank=True, max_length=20, null=True)),
                ('area', models.CharField(blank=True, max_length=50, null=True)),
                ('street_name', models.CharField(blank=True, max_length=150, null=True)),
                ('location_type', models.CharField(choices=[('1', 'Home'), ('2', 'Business')], max_length=10)),
                ('phone', models.CharField(blank=True, max_length=150, null=True)),
                ('country', models.CharField(blank=True, max_length=50, null=True)),
                ('shipping_note', models.CharField(blank=True, max_length=255, null=True)),
                ('building_name', models.CharField(blank=True, max_length=255, null=True)),
                ('floor_no', models.CharField(blank=True, max_length=255, null=True)),
                ('apartment_no', models.CharField(blank=True, max_length=255, null=True)),
                ('nearest_landmark', models.CharField(blank=True, max_length=255, null=True)),
                ('postal_code', models.CharField(blank=True, max_length=50, null=True)),
                ('slug', models.SlugField(unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Shipping Address',
                'ordering': ['updated_at'],
            },
        ),
    ]
