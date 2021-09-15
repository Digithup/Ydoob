# Generated by Django 3.2.6 on 2021-09-14 21:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('catalog', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='productreviewvoting',
            name='product_review_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.productreviews'),
        ),
        migrations.AddField(
            model_name='productreviewvoting',
            name='user_id_voting',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='productreviews',
            name='product_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.products'),
        ),
        migrations.AddField(
            model_name='productreviews',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='productquestions',
            name='product_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.products'),
        ),
        migrations.AddField(
            model_name='productquestions',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='productmedia',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.products'),
        ),
        migrations.AddField(
            model_name='productdiscount',
            name='product_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.products'),
        ),
        migrations.AddField(
            model_name='optionsdetails',
            name='option',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.options'),
        ),
        migrations.AddField(
            model_name='optionsdetails',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.products'),
        ),
        migrations.AddField(
            model_name='options',
            name='option_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='options_type', to='catalog.optionstype'),
        ),
        migrations.AddField(
            model_name='filters',
            name='filter_group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.filtersgroup'),
        ),
        migrations.AddField(
            model_name='categories',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='catalog.categories'),
        ),
        migrations.AddField(
            model_name='attributesdetails',
            name='attribute',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.attributes'),
        ),
        migrations.AddField(
            model_name='attributesdetails',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.products'),
        ),
        migrations.AddField(
            model_name='attributes',
            name='attributes_group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.attributesgroup'),
        ),
    ]
