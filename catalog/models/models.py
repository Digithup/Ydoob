import os
import uuid

from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
# Create your models here.
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from translations.models import Translatable

from catalog.models.product_options import Filters, Manufacturer, Attributes, Options
from user.models import User

STATUS = (
    ('True', 'Yes'),
    ('False', 'NO'),
)

OutStock = (
    ('1', '2-3 Day'),
    ('2', 'In Stock'),
    ('3', 'Out Stock'),
    ('4', 'Pre-order'),
)


class Categories(MPTTModel, Translatable):
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    title = models.CharField(verbose_name=_('title'),
                             help_text=_('the title of the continent'),
                             max_length=64, )
    keywords = models.CharField(max_length=255)
    description = RichTextUploadingField()
    image = models.ImageField(blank=True, upload_to='images/category/%Y/%m/%d')
    status = models.CharField(max_length=10, choices=STATUS)

    slug = models.SlugField(null=False, max_length=128, unique=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        # ordering = ('title',)
        verbose_name = 'category'
        # verbose_name_plural = 'categories'

    class MPTTMeta:
        order_insertion_by = ['title']

    class TranslatableMeta:
        fields = ['title', ]

    def get_absolute_url(self):
        return reverse("category_list")

    def __str__(self):
        return self.title




class Products(models.Model):
    id = models.AutoField(primary_key=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, null=False)
    title = models.CharField(max_length=255, null=False, blank=False)
    keyword = models.CharField(max_length=255, null=False, blank=False)
    long_desc = models.TextField(null=True)
    model = models.CharField(max_length=65, null=True)
    brand = models.CharField(max_length=255, null=True)
    price = models.CharField(max_length=255, null=False)
    quantity = models.CharField(max_length=255, default=0)
    minimum_quantity = models.CharField(max_length=255, default=1)
    subtract_stock = models.CharField(max_length=255, choices=STATUS, default='Yes', null=True)
    out_of_stock_status = models.CharField(max_length=255, choices=OutStock, default='2')
    requires_shipping = models.CharField(max_length=65, default=False, choices=STATUS, null=True)
    weight = models.IntegerField(default=0, null=True, blank=True)
    length = models.IntegerField(default=0, null=True, blank=True)
    filter = models.ManyToManyField(Filters, related_name="product_filter", blank=True)
    manufacturer = models.ManyToManyField(Manufacturer, related_name="product_manufacturer", blank=True)
    related = models.ManyToManyField('self', related_name="product_manufacturer", blank=True)


    status = models.CharField(max_length=10, null=True)
    sort_order = models.SmallIntegerField(default=0, null=True)
    slug = models.SlugField(unique=True, null=False, max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('ProductDetail', args=[str(self.id)])

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


def image_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:8], ext)
    sub_folder = 'file'
    if ext.lower() in ["jpg", "png", "gif"]:
        sub_folder = "avatar"
    if ext.lower() in ["pdf", "docx"]:
        sub_folder = "document"
    return os.path.join(instance.product, sub_folder, filename)


class AttributesDetails(models.Model):
    attribute = models.ManyToManyField(Attributes, related_name="product_attribute", blank=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, null=True)
    attribute_detail = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.attribute

    class Meta:
        verbose_name_plural = "Attribute Detail"

class OptionsDetails(models.Model):
    option = models.ManyToManyField(Options, related_name="product_options", blank=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, null=True)
    option_detail = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.option

    class Meta:
        verbose_name_plural = "Options"


class ProductMedia(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    image = models.FileField(verbose_name='Product Image', name='Image', upload_to='images/products/%Y/%m/')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["product"]
        verbose_name_plural = "Product Image"


class ProductTransaction(models.Model):
    id = models.AutoField(primary_key=True)
    transaction_type_choices = ((1, "BUY"), (2, "SELL"))
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    transaction_product_count = models.IntegerField(default=1)
    transaction_type = models.CharField(choices=transaction_type_choices, max_length=255)
    transaction_description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)


class ProductDiscount(models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    discount_title = models.CharField(max_length=255, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    priority = models.CharField(max_length=255, null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    data_start = models.DateTimeField(null=True, blank=True)
    data_end = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False, null=True, blank=True)


class ProductTags(models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    meta_title = models.CharField(max_length=255, verbose_name='Meta Tag Title')
    meta_description = models.CharField(max_length=255)
    meta_keywords = models.CharField(max_length=255)
    tags = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS)


class ProductQuestions(models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS)


class ProductReviews(models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    review_image = models.FileField()
    rating = models.CharField(default="5", max_length=255)
    review = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS)


class ProductReviewVoting(models.Model):
    id = models.AutoField(primary_key=True)
    product_review_id = models.ForeignKey(ProductReviews, on_delete=models.CASCADE)
    user_id_voting = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS)


class ProductVariant(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)


class ProductVariantItems(models.Model):
    id = models.AutoField(primary_key=True)
    product_variant_id = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
