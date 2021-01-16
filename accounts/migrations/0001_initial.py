# Generated by Django 3.1.4 on 2021-01-16 15:22

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('first_name', models.CharField(blank=True, max_length=200, null=True)),
                ('last_name', models.CharField(blank=True, max_length=200, null=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('address', models.CharField(blank=True, max_length=150, null=True)),
                ('city', models.CharField(blank=True, max_length=20, null=True)),
                ('country', models.CharField(blank=True, max_length=50, null=True)),
                ('image', models.ImageField(blank=True, default='images/dashboard/man.png', null=True, upload_to='images/users/')),
                ('facebook', models.URLField(blank=True, max_length=50)),
                ('instagram', models.URLField(blank=True, max_length=50)),
                ('twitter', models.URLField(blank=True, max_length=50)),
                ('youtube', models.URLField(blank=True, max_length=50)),
                ('about', ckeditor_uploader.fields.RichTextUploadingField(blank=True)),
                ('active', models.BooleanField(default=True)),
                ('customer', models.BooleanField(default=False)),
                ('seller', models.BooleanField(default=False)),
                ('staff', models.BooleanField(default=False)),
                ('admin', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
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
    ]
