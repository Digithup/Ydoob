import os
import uuid

from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.text import slugify

from localization.models.models import Country, Governorates, City, Area

User = get_user_model()

class Vendor(models.Model):
    STATUS = (
        ('True', 'Enable'),
        ('False', 'Disable'),
    )
    id = models.AutoField(primary_key=True)
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, blank=True ,)
    title = models.CharField(max_length=150 , null=False,blank=False ,default=' ' ,)
    email = models.EmailField( max_length=50,  null=False,blank=False , unique=True, verbose_name='Vendor Email')
    phone = models.IntegerField(null=False,blank=False , default='510', verbose_name='Vendor Phone')
    company = models.CharField(max_length=50, default=' ',null=False,blank=False ,)
    about = RichTextUploadingField(blank=True, default='', null=True)
    keywords = models.CharField(max_length=255 , default=' ' , null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    governorates = models.ForeignKey(Governorates, on_delete=models.CASCADE,default='1')
    city = models.ForeignKey(City, on_delete=models.CASCADE,default='1')
    area = models.ForeignKey(Area, on_delete=models.CASCADE,null=True,blank=True)
    address = models.CharField(blank=True, max_length=100 , default=' ', null=True)
    facebook = models.URLField(blank=True, max_length=50 , default='', null=True)
    instagram = models.URLField(blank=True, max_length=50 , default='', null=True)
    twitter = models.URLField(blank=True, max_length=50 , default='', null=True)
    youtube = models.URLField(blank=True, max_length=50 , default='', null=True)
    status = models.BooleanField(default=False)
    activation = models.BooleanField(default=False)
    code = models.CharField(max_length=255, editable=False,)
    slug = models.SlugField(null=False, blank=False, unique=True)
    create_at = models.DateTimeField(auto_now=True ,null=False)
    update_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Vendor, self).save(*args, **kwargs)

        ## method to create a fake table field in read only mode
    def image_tag(self):
        if self.image.url is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
        else:
            return ""

    def get_absolute_url(self):
        view_name = "vendor:detail_slug"
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
    store_id=models.ForeignKey(Vendor, on_delete=models.CASCADE, )
    media_content=models.FileField(upload_to=image_directory_path ,verbose_name="Vendor Logo" )
    created_at=models.DateTimeField(auto_now_add=True)
    is_active=models.IntegerField(default=1)






