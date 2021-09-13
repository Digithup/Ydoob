from django.db import models


# Create your models here.
class Home(models.Model):
    title = models.CharField(max_length=10,default='Nigne')
    content = models.CharField(max_length=300,default="")
    slug = models.SlugField(max_length=30, unique=True,default='nigne')

    def __str__(self):
        return self.title


class Language(models.Model):
    name = models.CharField(max_length=20, unique=True, default='English')
    code = models.CharField(max_length=5, unique=True,default='en')
    image = models.ImageField(upload_to='images/lang/%Y/%m/%d', null=True, default='images/lang/en-gb.png')
    status = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


