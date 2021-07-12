# Generated by Django 3.1.7 on 2021-07-11 16:31

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banners',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('True', 'Enable'), ('False', 'Disable')], max_length=10)),
                ('title', models.CharField(max_length=150, unique=True, verbose_name='Title')),
                ('sort_order', models.IntegerField(default=0)),
                ('media_content', models.FileField(upload_to='images/banners')),
                ('media_link', models.URLField(blank=True)),
                ('media_location', models.CharField(max_length=100)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20, unique=True)),
                ('is_active', models.PositiveSmallIntegerField()),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.IntegerField(blank=True, default='510')),
                ('email', models.EmailField(blank=True, default='', max_length=50, null=True)),
                ('facebook', models.URLField(blank=True, default='', max_length=50, null=True)),
                ('instagram', models.URLField(blank=True, default='', max_length=50, null=True)),
                ('twitter', models.URLField(blank=True, default='', max_length=50, null=True)),
                ('youtube', models.URLField(blank=True, default='', max_length=50, null=True)),
                ('status', models.CharField(choices=[('True', 'Enable'), ('False', 'Disable')], default='Enable', max_length=10)),
                ('create_at', models.DateTimeField(auto_now=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('True', 'Enable'), ('False', 'Disable')], max_length=10)),
                ('title', models.CharField(max_length=150, unique=True, verbose_name='Title')),
                ('sort_order', models.IntegerField(default=0)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='SliderGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='the title of the continent', max_length=64, unique=True, verbose_name='title')),
                ('status', models.CharField(choices=[('True', 'Enable'), ('False', 'Disable')], max_length=10)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='SliderMedia',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('media_type', models.CharField(max_length=255)),
                ('media_content', models.FileField(upload_to='images/slider')),
                ('media_link', models.URLField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('slider_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.slider')),
            ],
        ),
        migrations.AddField(
            model_name='slider',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.slidergroup'),
        ),
        migrations.CreateModel(
            name='SettingMedia',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('media_type', models.CharField(max_length=255)),
                ('media_content', models.FileField(upload_to='images/setting')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.IntegerField(default=1)),
                ('setting_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.setting')),
            ],
        ),
        migrations.CreateModel(
            name='SettingLang',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lang', models.CharField(default='en', max_length=6)),
                ('title', models.CharField(default='Nigne', max_length=150, null=True)),
                ('keywords', models.CharField(default=' ', max_length=255, null=True)),
                ('company', models.CharField(default=' ', max_length=50, null=True)),
                ('address', models.CharField(blank=True, default=' ', max_length=100, null=True)),
                ('about', ckeditor_uploader.fields.RichTextUploadingField(blank=True, default='', null=True)),
                ('contact', ckeditor_uploader.fields.RichTextUploadingField(blank=True, default='', null=True)),
                ('setting_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.setting')),
            ],
        ),
        migrations.CreateModel(
            name='MenuItems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=20)),
                ('url', models.CharField(max_length=20, null=True)),
                ('target', models.CharField(max_length=20)),
                ('position', models.IntegerField(null=True)),
                ('is_root', models.PositiveSmallIntegerField(default=0)),
                ('is_fluid', models.PositiveSmallIntegerField(default=0)),
                ('is_active', models.PositiveSmallIntegerField()),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.categories')),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.menu')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='core.menuitems')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=50)),
                ('image', models.ImageField(blank=True, upload_to='images/store/')),
                ('setting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.setting')),
            ],
        ),
    ]
