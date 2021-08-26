from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.sites.models import Site

from core.models.setting import Setting, SettingLang, SettingTags
from vendors.models import Store


class SettingForm(forms.ModelForm):
    class Meta:
        model = Setting
        fields = '__all__'


class SettingLangForm(forms.ModelForm):

    class Meta:
        model = SettingLang
        fields = '__all__'
        exclude = ('setting',)


class SettingTagForm(forms.ModelForm):
    class Meta:
        model = SettingTags
        fields = '__all__'
        exclude = ('setting',)

class SiteForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = '__all__'
