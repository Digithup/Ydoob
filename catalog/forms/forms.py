from ckeditor.widgets import CKEditorWidget
from django import forms

from catalog.models.models import Categories, Products, ProductMedia, AttributesDetails, OptionsDetails, VariantDetails
from catalog.models.product_options import Color, Size, OptionsType


class CategoryAddForm(forms.ModelForm):

    category_id = forms.IntegerField(required=False)

    class Meta:
        model = Categories
        fields = '__all__'


class ProductsForm(forms.ModelForm):
    # product_id = forms.IntegerField(required=False)
    category = forms.ModelChoiceField(queryset=Categories.objects.all(), label=u"Category", )
    # filter = forms.ModelChoiceField(queryset=Filters.objects.all(), label=u"Filter", required=False,
    #                                 widget=ModelSelect2Widget(
    #                                     search_fields=['title'], dependent_fields={'filters': 'filters'}))
    #
    # manufacturer = forms.ModelChoiceField(queryset=Manufacturer.objects.all(), required=False, label=u"manufacturer",
    #                                       widget=ModelSelect2Widget(
    #                                           search_fields=['title', 'image'],
    #                                           dependent_fields={'manufacturer': 'manufacturer'}))
    #
    # related = forms.ModelChoiceField(queryset=Products.objects.all(), required=False, label=u"related",
    #                                  widget=ModelSelect2Widget(
    #                                      search_fields=['title', 'image'],
    #                                      dependent_fields={'product_related': 'product_related', 'image': 'image'}))

    status = forms.ChoiceField(label="Status", choices=(
        ('True', 'Yae'),
        ('False', 'No'),))
    OutStock = (
        ('1', '2-3 Day'),
        ('2', 'In Stock'),
        ('3', 'Out Stock'),
        ('4', 'Pre-order'),
    )


    class Meta:
        model = Products
        fields = '__all__'
        # exclude=['seller']
        # extra_field = CategoryAddForm.Meta.fields
        widgets = {'title': forms.TextInput(attrs={'class': 'form-control'}),
                   'keywords': forms.TextInput(attrs={'class': 'form-control'}),
                   'category': forms.Select(attrs={'class': 'custom-select'}),
                   'subtract_stock': forms.Select(attrs={'class': 'custom-select'}),
                   'out_of_stock_status': forms.Select(attrs={'class': 'custom-select'}),
                   'slug': forms.TextInput(attrs={'class': 'form-control'}),
                   'price': forms.NumberInput(attrs={'class': 'form-control'}),
                   'long_desc': CKEditorWidget(attrs={'class': 'form-control'}),

                   }


class AttributesDetailsForm(forms.ModelForm):
    attribute_detail = forms.CharField(required=False)

    class Meta:
        model = AttributesDetails
        fields = '__all__'
        exclude = ['product']


class OptionsDetailsForm(forms.ModelForm):
    option_type = forms.ModelChoiceField(queryset=OptionsType.objects.all(), label=u"OptionsType",
                                    )

    option_price = forms.CharField(required=False)
    option_detail = forms.CharField(required=False)
    class Meta:
        model = OptionsDetails
        fields = '__all__'
        exclude = ['product']


class VariantDetailsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(VariantDetailsForm, self).__init__(*args, **kwargs)
        self.fields['size'].choices = list(Size.objects.values_list('id', 'name'))

        self.fields['color'].choices = list(Color.objects.values_list('id', 'name'))



    variant_detail = forms.CharField(required=False)
    variant_price = forms.CharField(required=False)
    variant_quantity = forms.CharField(required=False)
    variant_image = forms.CharField(required=False)
    class Meta:
        model = VariantDetails
        fields = '__all__'
        exclude = ['product']




class ProductMediaForm(forms.ModelForm):
    image = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    def __init__(self, *args, **kwargs):
        super(ProductMediaForm, self).__init__(*args, **kwargs)
        self.fields['image'].label = "Product Image"

    class Meta:
        model = ProductMedia
        fields = ['image']
        exclude = ['product']





class ColorForm(forms.ModelForm):

    class Meta:
        model = Color
        fields = '__all__'


class SizeForm(forms.ModelForm):
    class Meta:
        model = Size
        fields = '__all__'
