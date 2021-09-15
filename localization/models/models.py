from django.db import models


# Create your models here.
from django.template.defaultfilters import slugify

STATUS = (
    ('Yes', 'Yes'),
    ('NO', 'NO'),
)
class Home(models.Model):
    title = models.CharField(max_length=10,default='Nigne')
    content = models.CharField(max_length=300,default="")
    slug = models.SlugField(max_length=30, unique=True,default='nigne')


    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Home, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Language(models.Model):
    name = models.CharField(max_length=20, unique=True, default='English')
    code = models.CharField(max_length=5, unique=True,default='en')
    image = models.ImageField(upload_to='images/lang/%Y/%m/%d', null=True, default='images/lang/en-gb.png')
    status = models.CharField(max_length=10, choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


from django.db import models
from django.utils.text import slugify


class Country(models.Model):
    id = models.SmallIntegerField(primary_key=True, blank=False, null=False)
    name = models.CharField(max_length=30,default='Egypt')
    name_ar = models.CharField(max_length=30,default='مصر')
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Country, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Governorates(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=30,default='Qena')
    name_ar = models.CharField(max_length=30,default='قنا')
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Governorates, self).save(*args, **kwargs)
    def __str__(self):
        return self.name


class City(models.Model):

    governorates = models.ForeignKey(Governorates, on_delete=models.CASCADE)
    name = models.CharField(max_length=50,default='Qena')
    name_ar = models.CharField(max_length=50,default='Qena')
    slug = models.SlugField(unique=True)
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(City, self).save(*args, **kwargs)
    def __str__(self):
        return self.name



class Area(models.Model):
    id = models.SmallIntegerField(primary_key=True, blank=False, null=False)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    name = models.CharField(max_length=30,default='Qena')
    name_ar = models.CharField(max_length=30,default='Qena')
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Area, self).save(*args, **kwargs)
    def __str__(self):
        return self.name



