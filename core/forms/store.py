from django import forms
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.utils.text import slugify
from requests import request

from vendors.models import Vendor


class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields='__all__'
        widgets = {
                   'position': forms.Select(attrs={'class': 'custom-select'}),


                   }
