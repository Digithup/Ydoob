from django import forms
from django import forms
from django.forms import modelformset_factory

from core.models.design import Slider, SliderGroup, Banners


class BannerGroupAddForm(forms.ModelForm):
    class Meta:
        model = SliderGroup
        fields='__all__'





# class BannerAddForm(forms.ModelForm):
#     class Meta:
#         model = Slider
#
#         exclude = ['image','link','sort_order','caption']
#
#
# BannersFormSet = modelformset_factory(Slider, form=BannerAddForm, exclude=['groups', 'status'], extra=1, can_delete=True)


class BannersAddForm(forms.ModelForm):
    class Meta:
        model = Banners
        fields='__all__'
        widgets = {
                   'position': forms.Select(attrs={'class': 'custom-select'}),


                   }





