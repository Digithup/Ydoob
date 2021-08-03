
# Register your models here.
from mptt.admin import DraggableMPTTAdmin

from catalog.models.models import Categories, Products


class CategoryAdmin2(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title',
                    'related_products_count', 'related_products_cumulative_count')
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug': ('title',)}

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative catalog count
        qs = Categories.objects.add_related_count(
                qs,
                Products,
                'category',
                'products_cumulative_count',
                cumulative=True)

        # Add non cumulative catalog count
        qs = Categories.objects.add_related_count(qs,
                 Products,
                 'category',
                 'products_count',
                 cumulative=False)
        return qs
