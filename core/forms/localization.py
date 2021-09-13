from django.forms import ModelForm

from localization.models.models import Country


class AdminCountryForm(ModelForm):
    class Meta:
        model = Country
        exclude = ['slug']

