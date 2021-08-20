from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from imagekit.models import ProcessedImageField, ImageSpecField
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from pilkit.processors import ResizeToFill

from user.models import User

import os

from PIL import Image
from io import BytesIO

from django.core.files import File
from django.db.models import ImageField
from django.db.models.fields.files import ImageFieldFile
from django.utils.translation import ugettext_lazy as _

from catalog.models.models import Categories

STATUS = (
    ('True', 'Enable'),
    ('False', 'Disable'),
)


class SliderGroup(models.Model):
    title = models.CharField(verbose_name=_('title'),
                             help_text=_('the title of the continent'),
                             max_length=64, unique=True)
    status = models.CharField(max_length=10, choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Slider(models.Model):
    STATUS = (
        ('True', 'Enable'),
        ('False', 'Disable'),
    )
    group = models.ForeignKey(SliderGroup, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS)
    title = models.CharField(max_length=150, null=False, verbose_name="Title", unique=True)
    sort_order = models.IntegerField(default=0, null=False)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def status_verbose(self):
        return dict(Slider.STATUS)[self.status]


class SliderMedia(models.Model):
    id = models.AutoField(primary_key=True)
    slider_id = models.ForeignKey(Slider, on_delete=models.CASCADE)
    media_type_choice = ((1, "Image"), (2, "Video"))
    media_type = models.CharField(max_length=255)
    media_content = models.FileField(upload_to='images/slider')
    media_link = models.URLField(null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Banners(models.Model):
    STATUS = (
        ('True', 'Enable'),
        ('False', 'Disable'),
    )
    Position = (
        ('Top Left', 'Top Left'),
        ('Top Middle', 'Top Middle'),
        ('Top Right', 'Top Right'),
        ('Middle Left', 'Middle Left'),
        ('Middle Right', 'Middle Right'),
        ('Bottom Left', 'Bottom Left'),
        ('Bottom Middle', 'Bottom Middle'),
        ('Bottom Right', 'Bottom Right'),
        ('Collection Sidebar', 'Collection Sidebar'),
        ('Categories Top', 'Categories Top'),
        ('Categories Sidebar', 'Categories Sidebar'),
    )

    status = models.CharField(max_length=10, choices=STATUS,default="True")
    position = models.CharField(max_length=150, null=False, choices=Position, unique=True)

    media_content = models.FileField(upload_to='images/banners/%Y/%m/')
    media_link = models.URLField(null=False, blank=True)

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.position.title


class Menu(models.Model):
    title = models.CharField(max_length=20, unique=True, )
    is_active = models.PositiveSmallIntegerField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

class MenuItems(MPTTModel):
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE , null=True)
    type = models.CharField(max_length=20,  )
    url = models.CharField(max_length=20, null=True )
    target = models.CharField(max_length=20,  )
    position = models.IntegerField( null=True, )
    is_root = models.PositiveSmallIntegerField( default=0 )
    is_fluid = models.PositiveSmallIntegerField( default=0 )
    is_active = models.PositiveSmallIntegerField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
