from django.core.files.storage import FileSystemStorage
from django.http import request, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView

from catalog.models.models import Categories, Products, ProductMedia, ProductTags, ProductTransaction
from user.models import User


class ProductCreateTest3(CreateView):
    def get(self, request, *args, **kwargs):
        print(request)
        category = Categories.objects.filter(status=True)
        sellers = request.user.id


        return render(request, "vendor/catalog/product/add-product.html", {"categories": category, "sellers": sellers})

        #return render(request, "catalog/product/add-product.html", {"categories": category,"sellers": sellers })


    print(request)

    def post(self, request, *args, **kwargs):
        seller = request.POST.get("seller")
        category = request.POST.get("category")
        title = request.POST.get("title")
        description = request.POST.get("description")
        model = request.POST.get("model")
        brand = request.POST.get("brand")
        price = request.POST.get("price")
        quantity = request.POST.get("quantity")
        out_of_stock_status = request.POST.get("out_of_stock_status")
        requires_shipping = request.POST.get("requires_shipping")
        weight = request.POST.get("weight")
        length = request.POST.get("length")
        status = request.POST.get("status")
        slug = request.POST.get("slug")
        media_type_list = request.POST.getlist("media_type[]")
        media_content_list = request.FILES.getlist("media_content[]")
        product_tags = request.POST.get("product_tags")
        category = Categories.objects.get(id=category)
        seller = User.objects.get(id=seller)
        print(request.POST)

        product = Products(seller=seller, category=category, title=title, description=description,
                           model=model, brand=brand, price=price, quantity=quantity,
                           out_of_stock_status=out_of_stock_status,
                           requires_shipping=requires_shipping, weight=weight, length=length, status=status,
                           slug=slug)
        product.save()

        i = 0
        for media_content in media_content_list:
            fs = FileSystemStorage()
            filename = fs.save(media_content.name, media_content)
            media_url = fs.url(filename)
            product_media = ProductMedia(product_id=product, media_type=media_type_list[i], media_content=media_url)
            product_media.save()
            i = i + 1

        j = 0

        product_tags_list = product_tags.split(",")

        for product_tag in product_tags_list:
            product_tag_obj = ProductTags(product_id=product, title=product_tag)
            product_tag_obj.save()

        product_transaction = ProductTransaction(product_id=product, transaction_type=1,
                                                 transaction_product_count=quantity,
                                                 transaction_description="Initially Item Added in Stocks")
        print(request.POST)
        product_transaction.save()
        return HttpResponse("OK")
        #return redirect(reverse('vendors:ProductsList'))

