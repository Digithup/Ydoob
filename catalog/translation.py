from modeltranslation.translator import translator, TranslationOptions

from catalog.models.models import Categories



class CategoryTranslationOptions(TranslationOptions):
    fields = ('title',)

translator.register(Categories, CategoryTranslationOptions)
