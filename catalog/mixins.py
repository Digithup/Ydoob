from django.http import Http404

from djangodm.mixins import LoginRequiredMixin
from sellers.mixins import SellerAccountMixin

class ProductsManagerMixin(SellerAccountMixin, object):
    def get_object(self, *args, **kwargs):
        seller = self.get_account()
        obj = super(ProductsManagerMixin, self).get_object(*args, **kwargs)
        try:
            obj.seller == seller
        except:
            raise Http404
        if obj.seller == seller:
            return obj
        else:
            raise Http404
