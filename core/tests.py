from django.contrib import messages
from django.forms import modelformset_factory
from django.http import request
from django.shortcuts import redirect
from django.views import View

from core.forms.banners_forms import BannerAddForm, render
from core.models.banners import Banners
from localization.models import Language


def banner_create(request):
    qs = Banners.objects.none()
    BannersFormSet = modelformset_factory(Banners, form=BannerAddForm,exclude=['group','status'], extra=1,can_delete=True)

    if request.method == 'POST':
        banner_form = BannerAddForm(request.POST, prefix='banner')

        formset = BannersFormSet(request.POST ,request.FILES)

        if formset.is_valid() and banner_form.is_valid():
            # Generate a workday object
            banner = banner_form.save(commit=False)
            banner.group = banner_form.cleaned_data['group']
            banner.status = banner_form.cleaned_data['status']
            banner.save()

            # Generate entry objects for each form in the entry formset
            for form in formset:
                e = form.save(commit=False)
                e.banner = banner
                e.save()
                form.save_m2m()

                messages.add_message(request, messages.SUCCESS,
                                     "Banner add successfully " +
                                     e.banner.group +
                                     ": " + e.caption + " (" + str(e.group) +") - "
                )

            return redirect('core:BannerView')
        else:
            banner_form = BannerAddForm(request.POST, prefix='banner')
            formset = BannersFormSet(request.POST,request.FILES)

            for dict in formset.errors:
                messages.add_message(request, messages.ERROR, dict)

            context = {
                       'banner_form': banner_form,
                       'formset': formset,
                       }
            return render(request, 'banner/add-banners.html', context)

    else:
        banner_form = BannerAddForm(prefix='banner')
        formset = BannersFormSet(queryset=qs)
        context = {
                   'banner_form': banner_form,
                   'formset': formset,
                   }
        return render(request, 'banner/add-banners.html', context)

"""
<QueryDict: {'csrfmiddlewaretoken': ['BSshEbKdZt8Rdes9kzXUSOAT16IGOgD4WE4Cjw2zp6mqEujhAkoEJWkxdykNw3PJ'], 
'category_description[][name]': ['arabic', 'english'],
 'category_description[][description]': ['1', '2'],
  'category_description[][meta_title]': ['arabic', 'english'],
   'category_description[][meta_description]': ['1', '2'], 
   'category_description[][meta_keyword]': ['1', '2'], 
   'phone': ['5'], 'email': ['nigne@gmail.com'], 
   'facebook': ['https://www.facebook.com/'], 
   'instagram': ['https://www.facebook.com/'], 'twitter': ['https://www.facebook.com/'], 
   'youtube': ['https://www.facebook.com/'], 'media_type[]': ['1'], 
   'media_content[]': [''], 'slug': ['675'], 'status': ['True'], 'tags': ['5']}>

[22/Jun/2021 17:03:10] "POST /admin/setting/add/ HTTP/1.1" 200 60850
"""

class SettingAddView(View):
    def get(self, request, *args, **kwargs):
        print(request)
        language = Language.objects.filter(status=True)
        #sellers = User.objects.filter(seller=True)

        return render(request, "catalog/add-product.html",
                      {"language": language, })
    print(request)
    def post(self, request, *args, **kwargs):
        title = request.POST.get("title")
        brand = request.POST.get("brand")
        slug = request.POST.get("slug")
        category = request.POST.get("category")
        product_description = request.POST.get("product_description")
        long_desc = request.POST.get("long_desc")
        product_max_price = request.POST.get("product_max_price")
        product_discount_price = request.POST.get("product_discount_price")
        seller = request.POST.get("seller")
        in_stock_total = request.POST.get("in_stock_total")
        media_type_list = request.POST.getlist("media_type[]")
        media_content_list = request.FILES.getlist("media_content[]")
        title_title_list = request.POST.getlist("title_title[]")
        title_details_list = request.POST.getlist("title_details[]")
        about_title_list = request.POST.getlist("about_title[]")
        product_tags = request.POST.get("product_tags")

        #status = request.POST.get("status")



        product = Products(title=title, in_stock_total=in_stock_total, slug=slug, brand=brand,
                           product_description=product_description,category=category,
                           product_max_price=product_max_price, product_discount_price=product_discount_price,
                           product_long_description=long_desc,)
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
        for title_title in title_title_list:
            product_details = ProductDetails(title=title_title, title_details=title_details_list[j],
                                              product_id=product)
            product_details.save()
            j = j + 1

        for about in about_title_list:
            product_about = ProductAbout(title=about, product_id=product)
            product_about.save()

        product_tags_list = product_tags.split(",")

        for product_tag in product_tags_list:
            product_tag_obj = ProductTags(product_id=product, title=product_tag)
            product_tag_obj.save()

        product_transaction = ProductTransaction(product_id=product, transaction_type=1,
                                                  transaction_product_count=in_stock_total,
                                                  transaction_description="Intially Item Added in Stocks")
        product_transaction.save()
        return HttpResponse("OK")
        #return render(request, 'catalog/products-admin.html')