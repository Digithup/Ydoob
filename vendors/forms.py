from django import forms
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.utils.text import slugify
from requests import request

from localization.models.models import City, Governorates
from user.forms.forms import UserSignUpForm
from vendors.models import Vendor

User = get_user_model()

class SellerRegisterForm(forms.ModelForm):
    """
    Description:A form for creating new users.
    Includes all the required fields, plus a repeated password
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'phone', 'password1', 'password2']

    def already_user(self):
        user = User.objects.all()
        if user.is_authenticated:
            email = user.email
        else:
            email = self.cleaned_data.get("email")
        return email

    def clean_password2(self):
        """
        Description:Check that the two password entries match.\n
        """
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")

        return password2

    def save(self, commit=True):
        """
        Description:Save the provided password in hashed format.\n
        """
        user = super(SellerRegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        user.seller = True
        user.active = False  # send confirmation email via signals

        if commit:
            user.save()

        return user


class AlreadyUserSellerRegisterForm(forms.ModelForm):
    class Meta:
        model = User
        # fields = '__all__'
        fields = ['seller',]
        def save(self, commit=True):
            """
            Description:Save the provided password in hashed format.\n
            """
            user = super(AlreadyUserSellerRegisterForm, self).save(commit=False)
            user.seller = True
            user.active = False  # send confirmation email via signals
            if commit:
                user.save()
            return user


class CreateVendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        # fields = '__all__'
        fields = ['title', 'email', 'phone','company','country','governorates','city' ]
        def clean_title(self, title):
            email = slugify(title)
            if Vendor.objects.filter(email=email).exists():
                raise ValidationError('Vendor with this Email already exists.')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['governorates'].queryset = Governorates.objects.none()
        self.fields['city'].queryset = City.objects.none()

        if 'country' in self.data:
            try:
                country_id = int(self.data.get('country'))
                self.fields['governorates'].queryset = Governorates.objects.filter(country_id=country_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['governorates'].queryset = self.instance.country.city_set.order_by('name')
        if 'governorates' in self.data:
            try:
                governorates_id = int(self.data.get('governorates'))
                self.fields['city'].queryset = City.objects.filter(governorates_id=governorates_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['city'].queryset = self.instance.country.city_set.order_by('name')






class StoreAddFormm(forms.ModelForm):
    class Meta:
        model = Vendor

        # fields = '__all__'
        fields = ['email', 'phone', 'vendor']

        # exclude=['vendor']

    # exclude = ('vendor',)  # ETA: added comma to make this a tuple
    def user(self):

        user = User.objects.filter(pk=id)
        if user is None:
            messages.error(
                request, 'Account is not active,please check your email')
            return render(request, 'users/register/CustomerRegister.html', context={
                "title": "Register",
                "form": UserSignUpForm
            })
        else:
            def save(self, commit=True):
                obj = super(StoreAddFormm, self).save(False)
                # obj.vendor = User.objects.filter(vendor=)
                commit and obj.save()
                return obj


class StoreEditForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = '__all__'
