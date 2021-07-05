import datetime
from urllib import request

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field, Submit
from easy_select2.widgets import Select2
from ckeditor.fields import RichTextField
from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.forms import TextInput, EmailInput, Select, FileInput, Textarea, ImageField
from haystack import indexes

from catalog.models.models import Categories, Products, Image




class CategoryAddForm(forms.ModelForm):
    title = forms.CharField(widget=CKEditorWidget())
    category_id = forms.IntegerField(required=False)
    class Meta:
        model = Categories
        fields = '__all__'





class ProductsAddForm(forms.ModelForm):
    thumbnail = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False, label='image')
    status = forms.ChoiceField(label="status", choices=(
        ('True', 'Enable'),
        ('False', 'Disable'),))
    variant = forms.ChoiceField(label="variant",
        choices = (
        ('None', 'None'),
        ('Size', 'Size'),
        ('Color', 'Color'),
        ('Size-Color', 'Size-Color'),))





    class Meta:
        model = Products
        fields = '__all__'
        # extra_field = CategoryAddForm.Meta.fields
        widgets = {'title': forms.TextInput(attrs={'class': 'form-control'}),
                   'keywords': forms.TextInput(attrs={'class': 'form-control'}),
                   'category': forms.Select(attrs={'class': 'custom-select'}),
                   #'variant': forms.Select(attrs={'class': 'custom-select'}),
                   'slug': forms.TextInput(attrs={'class': 'form-control'}),
                   'price': forms.NumberInput(attrs={'class': 'form-control'}),
                   'detail': CKEditorWidget(attrs={'class': 'form-control'}),

                   }




class ProductsFullForm(ProductsAddForm):
    Products_id = forms.IntegerField(required=False)
    thumbnail = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False )
    image1 = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)
    tags = forms.CharField(max_length=50, required=False)

    class Meta(ProductsAddForm.Meta):
        fields = '__all__'
        field_classes=ProductsAddForm.Meta.fields

        widgets = {'title': forms.TextInput(attrs={'class': 'form-control'}),
                   'keywords': forms.TextInput(attrs={'class': 'form-control'}),
                   'category': forms.Select(attrs={'class': 'custom-select'}),
                   #'variant': forms.Select(attrs={'class': 'custom-select'}),
                   'slug': forms.TextInput(attrs={'class': 'form-control'}),
                   'price': forms.NumberInput(attrs={'class': 'form-control'}),
                   'detail': CKEditorWidget(attrs={'class': 'form-control'}),

                   }

    def save(self, *args, **kwargs):
        image = super(ProductsFullForm, self).save(*args, **kwargs)
        if hasattr(self.files, 'getlist'):
            for f in self.files.getlist('image'):
                Image.objects.create(Products=image, image=f)
        return image




class ProductsIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    category = indexes.CharField(model_attr='catalog')
    pub_date = indexes.DateTimeField(model_attr='pub_date')

    def get_model(self):
        return Products

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(pub_date__lte=datetime.datetime.now())
