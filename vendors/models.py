import os
import uuid

from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.base_user import AbstractBaseUser
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe

from user.models import User, UserManager


class Store(models.Model):
    STATUS = (
        ('True', 'Enable'),
        ('False', 'Disable'),
    )
    id = models.AutoField(primary_key=True)
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, blank=True ,)
    title = models.CharField(max_length=150 , null=True ,default='Nigne' ,)
    email = models.EmailField( max_length=50,  null=True, unique=True, verbose_name='Store Email')
    phone = models.IntegerField(blank=True, default='510', verbose_name='Store Phone')
    company = models.CharField(max_length=50, default=' ', null=True)
    about = RichTextUploadingField(blank=True, default='', null=True)
    keywords = models.CharField(max_length=255 , default=' ' , null=True)
    slug = models.SlugField(null=False)
    country = models.CharField(blank=True, max_length=100, default=' ', null=True)
    city = models.CharField(blank=True, max_length=100, default=' ', null=True)
    address = models.CharField(blank=True, max_length=100 , default=' ', null=True)
    facebook = models.URLField(blank=True, max_length=50 , default='', null=True)
    instagram = models.URLField(blank=True, max_length=50 , default='', null=True)
    twitter = models.URLField(blank=True, max_length=50 , default='', null=True)
    youtube = models.URLField(blank=True, max_length=50 , default='', null=True)
    status = models.BooleanField(default=False)
    activation = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now=True ,null=False)
    update_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title

        ## method to create a fake table field in read only mode
    def image_tag(self):
        if self.image.url is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
        else:
            return ""

    def get_absolute_url(self):
        view_name = "store:detail_slug"
        return reverse(view_name, kwargs={"slug": self.slug})


def image_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:8], ext)
    sub_folder = 'file'
    if ext.lower() in ["jpg", "png", "gif"]:
        sub_folder = "avatar"
    if ext.lower() in ["pdf", "docx"]:
        sub_folder = "document"
    return os.path.join(instance.store_id.title, sub_folder, filename)

class StoreMedia(models.Model):
    id=models.AutoField(primary_key=True)
    store_id=models.ForeignKey(Store,on_delete=models.CASCADE ,)
    media_type_choice=((1,"Image"),(2,"Video"))
    media_type=models.CharField(max_length=255)
    media_content=models.FileField(upload_to=image_directory_path ,verbose_name="Store Logo" )
    created_at=models.DateTimeField(auto_now_add=True)
    is_active=models.IntegerField(default=1)






