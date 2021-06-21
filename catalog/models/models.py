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
    title = models.CharField(max_length=255)
    category=models.ForeignKey(Categories,on_delete=models.CASCADE)
    Products_description = models.TextField()
    Products_long_description = models.TextField()
    brand=models.CharField(max_length=255)
    Products_max_price=models.CharField(max_length=255)
    Products_discount_price=models.CharField(max_length=255)
    store=models.OneToOneField(Store,on_delete=models.CASCADE)
    in_stock_total=models.IntegerField(default=1)
    is_active=models.IntegerField(default=1)
    url_slug = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

class ProductsMedia(models.Model):
    id=models.AutoField(primary_key=True)
    Products_id=models.ForeignKey(Products,on_delete=models.CASCADE)
    media_type_choice=((1,"Image"),(2,"Video"))
    media_type=models.CharField(max_length=255)
    media_content=models.FileField()
    created_at=models.DateTimeField(auto_now_add=True)
    is_active=models.IntegerField(default=1)

class ProductsTransaction(models.Model):
    id=models.AutoField(primary_key=True)
    transaction_type_choices=((1,"BUY"),(2,"SELL"))
    Products_id=models.ForeignKey(Products,on_delete=models.CASCADE)
    transaction_Products_count=models.IntegerField(default=1)
    transaction_type=models.CharField(choices=transaction_type_choices,max_length=255)
    transaction_description=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)


class ProductsDetails(models.Model):
    id=models.AutoField(primary_key=True)
    Products_id=models.ForeignKey(Products,on_delete=models.CASCADE)
    title=models.CharField(max_length=255)
    title_details=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    is_active=models.IntegerField(default=1)

class ProductsAbout(models.Model):
    id=models.AutoField(primary_key=True)
    Products_id=models.ForeignKey(Products,on_delete=models.CASCADE)
    title=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    is_active=models.IntegerField(default=1)

class ProductsTags(models.Model):
    id=models.AutoField(primary_key=True)
    Products_id=models.ForeignKey(Products,on_delete=models.CASCADE)
    title=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    is_active=models.IntegerField(default=1)

class ProductsQuestions(models.Model):
    id=models.AutoField(primary_key=True)
    Products_id=models.ForeignKey(Products,on_delete=models.CASCADE)
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    question=models.TextField()
    answer=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    is_active=models.IntegerField(default=1)

class ProductsReviews(models.Model):
    id=models.AutoField(primary_key=True)
    Products_id=models.ForeignKey(Products,on_delete=models.CASCADE)
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    review_image=models.FileField()
    rating=models.CharField(default="5",max_length=255)
    review=models.TextField(default="")
    created_at=models.DateTimeField(auto_now_add=True)
    is_active=models.IntegerField(default=1)

class ProductsReviewVoting(models.Model):
    id=models.AutoField(primary_key=True)
    Products_review_id=models.ForeignKey(ProductsReviews,on_delete=models.CASCADE)
    user_id_voting=models.ForeignKey(User,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    is_active=models.IntegerField(default=1)

class ProductsVarient(models.Model):
    id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)

class ProductsVarientItems(models.Model):
    id=models.AutoField(primary_key=True)
    Products_varient_id=models.ForeignKey(ProductsVarient,on_delete=models.CASCADE)
    Products_id=models.ForeignKey(Products,on_delete=models.CASCADE)
    title=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
