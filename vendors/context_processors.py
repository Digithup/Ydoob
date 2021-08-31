from catalog.models.models import Products, ProductMedia
from vendors.models import Store, StoreMedia


def vendor_processors(request):


        store_owner = Store.objects.filter(vendor__id=request.user.id)

        vendor_store = []
        for store in store_owner:
                vendor_media = StoreMedia.objects.filter(store_id=store_owner[0],  is_active=1).first()
                vendor_store.append({"store": store, "vendor_media": vendor_media, })
        products_count = Products.objects.filter(seller__id=request.user.id).count()

        products = Products.objects.filter(seller__id=request.user.id)
        vendor_products_list = []
        for product in products:
                product_media = ProductMedia.objects.filter(product=product.id, ).first()
                vendor_products_list.append(
                        {"product": product, "product_media": product_media, "products_count": products_count})

        return {
                'store_owner': store_owner,
                'vendor_store': vendor_store,
                'vendor_products_list': vendor_products_list,



        }

