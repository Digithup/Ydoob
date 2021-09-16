from import_export import resources

from catalog.models.models import Products
from catalog.models.product_options import Color, Size


class ProductResource(resources.ModelResource):
    class Meta:
        model = Products


class ColorResource(resources.ModelResource):
    class Meta:
        model = Color

class SizeResource(resources.ModelResource):
    class Meta:
        model = Size
