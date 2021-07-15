import datetime

from ckeditor.widgets import CKEditorWidget
from django import forms
from haystack import indexes

from catalog.models.models import Categories, Products, ProductMedia


class CategoryAddForm(forms.ModelForm):
    title = forms.CharField(widget=CKEditorWidget())
    category_id = forms.IntegerField(required=False)
    class Meta:
        model = Categories
        fields = '__all__'



class ProductsForm(forms.ModelForm):
    #product_id = forms.IntegerField(required=False)

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
        #exclude=['seller']
        # extra_field = CategoryAddForm.Meta.fields
        widgets = {'title': forms.TextInput(attrs={'class': 'form-control'}),
                   'keywords': forms.TextInput(attrs={'class': 'form-control'}),
                   'category': forms.Select(attrs={'class': 'custom-select'}),
                   'subtract_stock':forms.Select(attrs={'class': 'custom-select'}),
                   'out_of_stock_status': forms.Select(attrs={'class': 'custom-select'} ),
                   'slug': forms.TextInput(attrs={'class': 'form-control'}),
                   'price': forms.NumberInput(attrs={'class': 'form-control'}),
                   'long_desc': CKEditorWidget(attrs={'class': 'form-control'}),

                   }

class ProductMediaForm(forms.ModelForm):
    image = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    def __init__(self, *args, **kwargs):
        super(ProductMediaForm, self).__init__(*args, **kwargs)
        self.fields['image'].label = "Product Image"

    class Meta:
        model = ProductMedia
        fields=['image']
        exclude=['product']









class ProductsIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    category = indexes.CharField(model_attr='catalog')
    pub_date = indexes.DateTimeField(model_attr='pub_date')

    def get_model(self):
        return Products

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(pub_date__lte=datetime.datetime.now())
