# Generated by Django 3.2.6 on 2021-09-22 01:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('province', models.CharField(default='Province 3', max_length=254)),
                ('district', models.CharField(default='Kathmandu', max_length=254)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(editable=False, max_length=5)),
                ('payment_status', models.CharField(choices=[('Pending', 'Pending'), ('Online Payment', 'Online Payment'), ('Cash on delivery', 'Cash on delivery')], default='Pending', max_length=100)),
                ('total', models.FloatField()),
                ('status', models.CharField(choices=[('New', 'New'), ('Accepted', 'Accepted'), ('Preparing', 'Preparing'), ('OnShipping', 'OnShipping'), ('Completed', 'Completed'), ('Canceled', 'Canceled')], default='New', max_length=10)),
                ('ordered', models.BooleanField(default=False)),
                ('email', models.CharField(max_length=100)),
                ('ip', models.CharField(blank=True, max_length=20)),
                ('adminnote', models.CharField(blank=True, max_length=100)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('price', models.FloatField()),
                ('amount', models.FloatField()),
                ('status', models.CharField(choices=[('New', 'New'), ('Accepted', 'Accepted'), ('Preparing', 'Preparing'), ('OnShipping', 'OnShipping'), ('Completed', 'Completed'), ('Canceled', 'Canceled')], default='New', max_length=10)),
                ('delivery_by', models.CharField(choices=[('Ydoob', 'Ydoob'), ('Self', 'Self')], default=False, max_length=10)),
                ('delivery_taken_datetime', models.DateTimeField(blank=True, null=True)),
                ('delivery_person_ip', models.GenericIPAddressField(blank=True, null=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('price', models.FloatField()),
                ('paid', models.BooleanField(default=False)),
                ('stripe_charge_id', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='PaymentMethods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('method', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('count', models.BigIntegerField(blank=True, default=0, null=True)),
                ('image', models.ImageField(blank=True, upload_to='images/payment_method/%Y/%m/%d')),
                ('status', models.CharField(choices=[('True', 'Yes'), ('False', 'NO')], default='False', max_length=10)),
                ('slug', models.SlugField(blank=True, default='COD', max_length=128, null=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ShopCart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('quantity', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.SmallIntegerField(default='1')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.products')),
            ],
        ),
    ]
