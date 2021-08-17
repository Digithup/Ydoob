from django.db import models

# Create your models here.
from django.utils.safestring import mark_safe

STATUS = (
    ('True', 'Yes'),
    ('False', 'NO'),
)


class FiltersGroup(models.Model):
    title = models.CharField(max_length=100, unique=True)
    sort_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


class Filters(models.Model):
    title = models.CharField(max_length=100, unique=True)
    filter_group = models.ForeignKey(FiltersGroup, on_delete=models.CASCADE, null=True)
    sort_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Filter"


class AttributesGroup(models.Model):
    title = models.CharField(max_length=100, )
    sort_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "AttributesGroup"


class Attributes(models.Model):
    title = models.CharField(max_length=100, unique=True)
    attributes_group = models.ForeignKey(AttributesGroup, on_delete=models.CASCADE, null=True)
    sort_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Attribute"


class OptionsType(models.Model):
    title = models.CharField(max_length=100, unique=True)
    sort_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Options Type"


class Options(models.Model):
    title = models.CharField(max_length=100, unique=True)
    option_type = models.ForeignKey(OptionsType, on_delete=models.CASCADE, null=True, related_name="options_type")
    sort_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Options"




class Color(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=10, blank=True,null=True)
    def __str__(self):
        return self.name
    def color_tag(self):
        if self.code is not None:
            return mark_safe('<p style="background-color:{}">Color </p>'.format(self.code))
        else:
            return ""

class Size(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=10, blank=True,null=True)
    def __str__(self):
        return self.name

class Manufacturer(models.Model):
    title = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='images/Manufacturer/%Y/', null=True, default='images/Manufacturer/en-gb.png')
    sort_order = models.IntegerField(default=0)
    slug = models.SlugField(null=title, unique=True)
    status = models.CharField(max_length=10, choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
