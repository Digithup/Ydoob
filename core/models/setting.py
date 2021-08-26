# Create your models here.


from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

# Create your models here.


class Setting(models.Model):
    STATUS = (
        ('True', 'Enable'),
        ('False', 'Disable'),
    )
    phone = models.IntegerField(blank=True, default='510')
    email = models.EmailField(blank=True, max_length=50, default='', null=True)
    image = models.ImageField(upload_to='images/setting/%Y/%m/%d',   default='images/store/nigne.png')
    facebook = models.URLField(blank=True, max_length=50, default='', null=True)
    instagram = models.URLField(blank=True, max_length=50, default='', null=True)
    twitter = models.URLField(blank=True, max_length=50, default='', null=True)
    youtube = models.URLField(blank=True, max_length=50, default='', null=True)
    status = models.CharField(max_length=10, choices=STATUS, default='Enable')
    slug = models.SlugField(unique=True,default='nigne')
    create_at = models.DateTimeField(auto_now=True, null=False)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email





class SettingLang(models.Model):
    setting = models.ForeignKey(Setting, on_delete=models.CASCADE)  # many to one relation with Category
    lang = models.CharField(max_length=6 , default='en' ,blank=True,null=True)
    title = models.CharField(max_length=150, null=True, default='Nigne')
    keywords = models.CharField(max_length=255, default=' ', null=True)
    company = models.CharField(max_length=50, default=' ', null=True)
    address = models.CharField(blank=True, max_length=100, default='', null=True)
    about = RichTextUploadingField(blank=True, default='', null=True)
    contact = RichTextUploadingField(blank=True, default='', null=True)
    #



class SettingTags(models.Model):
    id = models.AutoField(primary_key=True)
    setting = models.ForeignKey(Setting, on_delete=models.CASCADE)
    meta_title = models.CharField(max_length=255, verbose_name='Meta Tag Title')
    meta_description = models.CharField(max_length=255)
    meta_keywords = models.CharField(max_length=255)
    tags = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
