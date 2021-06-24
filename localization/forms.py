from modeltranslation.forms import TranslationModelForm

from localization.models import Home


class MyForm(TranslationModelForm):
    class Meta:
        model = Home