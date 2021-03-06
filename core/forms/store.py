from django import forms
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.text import slugify
from requests import request

from core.utils.utilities import notify_admin
from vendors.models import Vendor

User = get_user_model()

class AdminVendorForm(forms.ModelForm):
    keywords = forms.CharField(required=False)
    class Meta:
        model = Vendor
        fields='__all__'
        widgets = {
                   'position': forms.Select(attrs={'class': 'custom-select'}),    }




