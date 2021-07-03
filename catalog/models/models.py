from PIL import Image
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.translation import ugettext_lazy as _
from translations.models import Translatable
from django.core.files import File
from django.db import models
from django.db.models.signals import pre_save
from django.template.defaultfilters import slugify
# Create your models here.
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from six import BytesIO

from DNigne.utils import unique_slug_generator
from accounts.models import User
from vendors.models import Store

STATUS = (
    ('True', 'Enable'),
    ('False', 'Disable'),
)


class Categories(MPTTModel, Translatable):
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    title = models.CharField(verbose_name=_('title'),
                             help_text=_('the title of the continent'),
                             max_length=64, )
    keywords = models.CharField(max_length=255)
    description = RichTextUploadingField()
    image = models.ImageField(blank=True, upload_to='images/category')
    status = models.CharField(max_length=10, choices=STATUS)

    slug = models.SlugField(null=False, max_length=128, unique=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


    class Meta:
        # ordering = ('title',)
        verbose_name = 'category'
        #verbose_name_plural = 'categories'

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
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    product_max_price = models.CharField(max_length=255)
    product_discount_price = models.CharField(max_length=255)
    product_description = models.TextField()
    product_long_description = models.TextField()
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    in_stock_total = models.IntegerField(default=1)
    #status = models.CharField(max_length=10, choices=STATUS ,default='Enable')
    slug = models.SlugField(null=False, max_length=128, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class ProductMedia(models.Model):
    id=models.AutoField(primary_key=True)
    product_id=models.ForeignKey(Products,on_delete=models.CASCADE)
    media_type_choice=((1,"Image"),(2,"Video"))
    media_type=models.CharField(max_length=255)
    media_content=models.FileField()
    created_at=models.DateTimeField(auto_now_add=True)
    is_active=models.IntegerField(default=1)

class ProductTransaction(models.Model):
    id=models.AutoField(primary_key=True)
    transaction_type_choices=((1,"BUY"),(2,"SELL"))
    product_id=models.ForeignKey(Products,on_delete=models.CASCADE)
    transaction_product_count=models.IntegerField(default=1)
    transaction_type=models.CharField(choices=transaction_type_choices,max_length=255)
    transaction_description=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)


class ProductDetails(models.Model):
    id=models.AutoField(primary_key=True)
    product_id=models.ForeignKey(Products,on_delete=models.CASCADE)
    title=models.CharField(max_length=255)
    title_details=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS)

class ProductAbout(models.Model):
    id=models.AutoField(primary_key=True)
    product_id=models.ForeignKey(Products,on_delete=models.CASCADE)
    title=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS)

class ProductTags(models.Model):
    id=models.AutoField(primary_key=True)
    product_id=models.ForeignKey(Products,on_delete=models.CASCADE)
    title=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS)

class ProductQuestions(models.Model):
    id=models.AutoField(primary_key=True)
    product_id=models.ForeignKey(Products,on_delete=models.CASCADE)
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    question=models.TextField()
    answer=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS)

class ProductReviews(models.Model):
    id=models.AutoField(primary_key=True)
    product_id=models.ForeignKey(Products,on_delete=models.CASCADE)
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    review_image=models.FileField()
    rating=models.CharField(default="5",max_length=255)
    review=models.TextField(default="")
    created_at=models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS)

class ProductReviewVoting(models.Model):
    id=models.AutoField(primary_key=True)
    product_review_id=models.ForeignKey(ProductReviews,on_delete=models.CASCADE)
    user_id_voting=models.ForeignKey(User,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS)

class ProductVarient(models.Model):
    id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)

class ProductVarientItems(models.Model):
    id=models.AutoField(primary_key=True)
    product_varient_id=models.ForeignKey(ProductVarient,on_delete=models.CASCADE)
    product_id=models.ForeignKey(Products,on_delete=models.CASCADE)
    title=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
