from import_export import resources

from catalog.models.models import Products


class ProductResource(resources.ModelResource):
    class Meta:
        model = Products
