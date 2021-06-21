# Generated by Django 3.1.7 on 2021-06-19 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Home',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=10)),
                ('title_en', models.CharField(max_length=10, null=True)),
                ('title_ar', models.CharField(max_length=10, null=True)),
                ('content', models.CharField(max_length=300)),
                ('content_en', models.CharField(max_length=300, null=True)),
                ('content_ar', models.CharField(max_length=300, null=True)),
                ('slug', models.SlugField(max_length=30, unique=True)),
                ('slug_en', models.SlugField(max_length=30, null=True, unique=True)),
                ('slug_ar', models.SlugField(max_length=30, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('code', models.CharField(max_length=5, unique=True)),
                ('image', models.ImageField(default='images/lang/en-gb.png', null=True, upload_to='images/lang/%Y/%m/%d')),
                ('status', models.BooleanField()),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
