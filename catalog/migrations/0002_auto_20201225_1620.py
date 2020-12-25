# Generated by Django 3.1.4 on 2020-12-25 13:20

import catalog.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('image', models.ImageField(upload_to=catalog.models.get_upload_path)),
                ('default', models.BooleanField(default=False)),
                ('width', models.FloatField(default=100)),
                ('length', models.FloatField(default=100)),
            ],
        ),
        migrations.CreateModel(
            name='ImageAlbum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.DeleteModel(
            name='Images',
        ),
        migrations.AddField(
            model_name='image',
            name='album',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='catalog.imagealbum'),
        ),
        migrations.AddField(
            model_name='product',
            name='album',
            field=models.OneToOneField(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='model', to='catalog.imagealbum'),
            preserve_default=False,
        ),
    ]
