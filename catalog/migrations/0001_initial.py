# Generated by Django 3.2.6 on 2021-09-22 01:43

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attributes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
                ('sort_order', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Attribute',
            },
        ),
        migrations.CreateModel(
            name='AttributesDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attribute_detail', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Attribute Detail',
            },
        ),
        migrations.CreateModel(
            name='AttributesGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('sort_order', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'AttributesGroup',
            },
        ),
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('title_ar', models.CharField(max_length=255)),
                ('keywords', models.CharField(max_length=255)),
                ('description', ckeditor_uploader.fields.RichTextUploadingField()),
                ('image', models.ImageField(blank=True, upload_to='images/category/%Y/%m/%d')),
                ('status', models.CharField(choices=[('True', 'Yes'), ('False', 'NO')], max_length=10)),
                ('slug', models.SlugField(max_length=128, unique=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
            ],
            options={
                'verbose_name': 'category',
            },
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('code', models.CharField(blank=True, max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Filters',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
                ('sort_order', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Filter',
            },
        ),
        migrations.CreateModel(
            name='FiltersGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
                ('sort_order', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
                ('image', models.ImageField(default='images/Manufacturer/en-gb.png', null=True, upload_to='images/Manufacturer/%Y/')),
                ('sort_order', models.IntegerField(default=0)),
                ('slug', models.SlugField(null=models.CharField(max_length=100, unique=True), unique=True)),
                ('status', models.CharField(choices=[('True', 'Yes'), ('False', 'NO')], max_length=10)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Options',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
                ('sort_order', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Options',
            },
        ),
        migrations.CreateModel(
            name='OptionsDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option_detail', models.CharField(blank=True, max_length=255, null=True)),
                ('option_price', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Options Detail',
            },
        ),
        migrations.CreateModel(
            name='OptionsType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
                ('sort_order', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Options Type',
            },
        ),
        migrations.CreateModel(
            name='ProductDiscount',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('discount_title', models.CharField(blank=True, max_length=255, null=True)),
                ('quantity', models.IntegerField(blank=True, null=True)),
                ('priority', models.CharField(blank=True, max_length=255, null=True)),
                ('price', models.IntegerField(blank=True, null=True)),
                ('data_start', models.DateTimeField(blank=True, null=True)),
                ('data_end', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.BooleanField(blank=True, default=False, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductMedia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(upload_to='images/products/%Y/%m/', verbose_name='Product Image')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Product Image',
                'ordering': ['product'],
            },
        ),
        migrations.CreateModel(
            name='ProductQuestions',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('question', models.TextField()),
                ('answer', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('True', 'Yes'), ('False', 'NO')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='ProductReviews',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('review_image', models.FileField(upload_to='')),
                ('rating', models.CharField(default='5', max_length=255)),
                ('review', models.TextField(default='')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('True', 'Yes'), ('False', 'NO')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='ProductReviewVoting',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('True', 'Yes'), ('False', 'NO')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('is_featured', models.BooleanField(default=False)),
                ('title', models.CharField(max_length=1500)),
                ('keyword', models.CharField(max_length=3500)),
                ('long_desc', models.TextField(null=True)),
                ('model', models.CharField(max_length=65, null=True)),
                ('brand', models.CharField(max_length=255, null=True)),
                ('price', models.PositiveIntegerField(default=0)),
                ('quantity', models.CharField(default=0, max_length=255)),
                ('minimum_quantity', models.CharField(default=1, max_length=255)),
                ('subtract_stock', models.CharField(choices=[('True', 'Yes'), ('False', 'NO')], default='Yes', max_length=255, null=True)),
                ('out_of_stock_status', models.CharField(choices=[('1', '2-3 Day'), ('2', 'In Stock'), ('3', 'Out Stock'), ('4', 'Pre-order')], default='2', max_length=255)),
                ('requires_shipping', models.CharField(choices=[('True', 'Yes'), ('False', 'NO')], default=False, max_length=65, null=True)),
                ('weight', models.IntegerField(blank=True, default=0, null=True)),
                ('length', models.IntegerField(blank=True, default=0, null=True)),
                ('status', models.CharField(max_length=10, null=True)),
                ('variant', models.CharField(choices=[('None', 'None'), ('Size', 'Size'), ('Color', 'Color'), ('Size-Color', 'Size-Color')], default='None', max_length=10)),
                ('sort_order', models.SmallIntegerField(default=0, null=True)),
                ('slug', models.SlugField(blank=True, max_length=128, null=True, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.categories')),
                ('filter', models.ManyToManyField(blank=True, related_name='product_filter', to='catalog.Filters')),
                ('manufacturer', models.ManyToManyField(blank=True, related_name='product_manufacturer', to='catalog.Manufacturer')),
                ('related', models.ManyToManyField(blank=True, related_name='_catalog_products_related_+', to='catalog.Products')),
            ],
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('code', models.CharField(blank=True, max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Variants',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=12, null=True)),
                ('quantity', models.IntegerField(blank=True, default=1, null=True)),
                ('image', models.FileField(blank=True, null=True, upload_to='images/products/%Y/%m/', verbose_name='Product Image')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('color', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.color')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.products')),
                ('size', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.size')),
            ],
            options={
                'verbose_name_plural': 'Variant Detail',
            },
        ),
        migrations.CreateModel(
            name='ProductTransaction',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('transaction_product_count', models.IntegerField(default=1)),
                ('transaction_type', models.CharField(choices=[(1, 'BUY'), (2, 'SELL')], max_length=255)),
                ('transaction_description', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.products')),
            ],
        ),
        migrations.CreateModel(
            name='ProductTags',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('meta_title', models.CharField(max_length=255, verbose_name='Meta Tag Title')),
                ('meta_description', models.CharField(max_length=255)),
                ('meta_keywords', models.CharField(max_length=255)),
                ('tags', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('True', 'Yes'), ('False', 'NO')], max_length=10)),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.products')),
            ],
        ),
    ]
