from django.core.files.storage import FileSystemStorage
from django.http import request
from django.views import View

from core.forms.banners_forms import render
from core.models.setting import Setting, SettingLang, SettingMedia
from localization.models import Language

"""

def banner_create(request):
    qs = Slider.objects.none()
    BannersFormSet = modelformset_factory(Slider, form=BannerAddForm, exclude=['group', 'status'], extra=1,
                                          can_delete=True)

    if request.method == 'POST':
        banner_form = BannerAddForm(request.POST, prefix='design')

        formset = BannersFormSet(request.POST, request.FILES)

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
                                     ": " + e.caption + " (" + str(e.group) + ") - "
                                     )

            return redirect('core:BannerView')
        else:
            banner_form = BannerAddForm(request.POST, prefix='design')
            formset = BannersFormSet(request.POST, request.FILES)

            for dict in formset.errors:
                messages.add_message(request, messages.ERROR, dict)

            context = {
                'banner_form': banner_form,
                'formset': formset,
            }
            return render(request, 'design/add-banner.html', context)

    else:
        banner_form = BannerAddForm(prefix='design')
        formset = BannersFormSet(queryset=qs)
        context = {
            'banner_form': banner_form,
            'formset': formset,
        }
        return render(request, 'design/add-banner.html', context)




        
        
def AddProductVielw(request):
    if request.method == "POST":
        form = ProductsFullForm(request.POST or None, request.FILES or None)
        files = request.FILES.getlist('images')
        if form.is_valid():
            print(request.POST)
            product_created = True
            title = form.cleaned_data['title']
            keywords = form.cleaned_data['keywords']
            description = form.cleaned_data['description']
            thumbnail = form.cleaned_data['thumbnail']
            image1 = form.cleaned_data['image1']
            image2 = form.cleaned_data['image2']
            image3 = form.cleaned_data['image3']
            image4 = form.cleaned_data['image4']
            image5 = form.cleaned_data['image5']
            image6 = form.cleaned_data['image6']
            category = form.cleaned_data['category']
            variant = form.cleaned_data['variant']
            price = form.cleaned_data['price']
            sale_price = form.cleaned_data['sale_price']
            discount = form.cleaned_data['discount']
            amount = form.cleaned_data['amount']
            min_amount = form.cleaned_data['min_amount']
            detail = form.cleaned_data['detail']
            slug = form.cleaned_data['slug']
            status = form.cleaned_data['status']
            product_id = form.cleaned_data['product_id']
            tags = tagsInDic(form.cleaned_data['tags'].strip())
            tags_dic = tags.copy()
            if not product_id:
                print(request)
                product_obj = Products.objects.create(title=title, keywords=keywords, category=category,
                                                      description=description, variant=variant,
                                                      image1=image1, image2=image2, image3=image3, image4=image4,
                                                      image5=image5, image6=image6,
                                                      thumbnail=thumbnail, price=price, sale_price=sale_price,
                                                      discount=discount,
                                                      amount=amount, min_amount=min_amount, detail=detail,
                                                      slug=slug, status=status
                                                      )  # create will create as well as save too in db.
                for k in tags.keys():
                    tag_obj, created = Products.objects.get_or_create(name=k)
                    product_obj.tags.add(tag_obj)  # it won't add duplicated as stated in django docs
            else:
                # handling all cases of the tags
                print(request)
                product_obj = Products.objects.get(id=product_id)
                for t in product_obj.tags.all():
                    if t.name not in tags_dic:
                        product_obj.tags.remove(t)
                    else:  # deleting pre-existing element so that we could know what's new tags are
                        del tags_dic[t.name]
                for k, v in tags_dic.items():
                    tag_obj, created = Products.objects.get_or_create(name=k)
                    product_obj.tags.add(tag_obj)
                product_created = False
            for f in files:
                print(request)
                Image.objects.create(product=product_obj, image=f)
            product_obj.category = category
            product_obj.variant = variant
            product_obj.title = title
            product_obj.keywords = keywords
            product_obj.description = description
            product_obj.thumbnail = thumbnail
            product_obj.image1 = image1
            product_obj.image2 = image2
            product_obj.image3 = image3
            product_obj.image4 = image4
            product_obj.image5 = image5
            product_obj.image6 = image6
            product_obj.price = price
            product_obj.sale_price = sale_price
            product_obj.discount = discount
            product_obj.amount = amount
            product_obj.min_amount = min_amount
            product_obj.detail = detail
            product_obj.slug = slug
            product_obj.status = status
            print(request.POST)
            product_obj.save()  # last_modified field won't update on chaning other model field, save() trigger change
            # return reverse('core:catalog')
            return HttpResponseRedirect('/admin/products', product_created)
            # return render(request,template_name='admin/pages/vendor-products.html')
            # return getNoteResponseData(product_obj, tags, product_created)
        else:
            print("Form invalid, see below error msg")
            print(request.POST)
            print(form.errors)
            messages.error(request, "Error")
    # if GET method form, or anything wrong then we will create blank form
    else:
        form = ProductsFullForm()
    # return HttpResponseRedirect('/')
    return render(request, 'catalog/product/admin-user-create.html', {'form': form})


class ProductAddViewTest(View):
    def get(self, request, *args, **kwargs):
        print(request)
        category = Categories.objects.filter(status=True)
        sellers = User.objects.filter(seller=True)

        return render(request, "catalog/product/product_create.html",
                      {"categories": category, "sellers": sellers})

    def post(request):
        if reque:
            print(request)
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
            print(request.POST)

            # status = request.POST.get("status")

            category = Categories.objects.get(id=category)
            seller = User.objects.get(id=seller)
            product = Products(title=title, in_stock_total=in_stock_total, slug=slug, brand=brand,
                               product_description=product_description, category=category,
                               product_max_price=product_max_price, product_discount_price=product_discount_price,
                               product_long_description=long_desc, seller=seller)
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
            # return HttpResponse("OK")
            print(request)
            return render(request, 'catalog/product/vendor-products.html')

            # return render(request,template_name='admin/pages/Products-admin.html')
            # return getNoteResponseData(Products_obj, tags, Products_created)
        else:

            print(request)
            messages.error(request, "Error")
            category = Categories.objects.filter(status=True)
            sellers = User.objects.filter(seller=True)

            return render(request, "catalog/product/product_create.html",
                          {"categories": category, "sellers": sellers})
         


        
        
"""

class SettingAddViewTest(View):
    def get(self, request, *args, **kwargs):
        print(request)
        langlist = Language.objects.filter(status=True)
        return render(request, 'setting/add-setting.html',
                      {"langlist": langlist, })

    print(request)

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        # image = request.POST.get('image')
        facebook = request.POST.get('facebook')
        instagram = request.POST.get('instagram')
        twitter = request.POST.get('twitter')
        youtube = request.POST.get('youtube')
        status = request.POST.get('status')
        setting_id = request.POST.get('setting_id')
        media_content_list = request.FILES.getlist("media_content[]")
        media_type_list = request.POST.getlist("media_type[]")
        setting_title_list = request.POST.getlist("title[]")
        setting_keywords_list = request.POST.getlist("keywords[]")
        setting_company_list = request.POST.getlist("company[]")
        setting_about_list = request.POST.getlist("about[]")
        setting_address_list = request.POST.getlist("address[]")
        setting_lang_list = request.POST.getlist("lang[]")
        print(request.POST)

        # status = request.POST.get("status")

        langlist = Language.objects.filter(status=True)

        setting_obj = Setting.objects.create(email=email, phone=phone,
                                             facebook=facebook, instagram=instagram,
                                             twitter=twitter, youtube=youtube, status=status,
                                             )  # create will create as well as save too in db.
        setting_obj.save()

        i = 0
        for media_content in media_content_list:
            fs = FileSystemStorage()
            filename = fs.save(media_content.name, media_content)
            media_url = fs.url(filename)

            setting_media = SettingMedia(setting_id=setting_obj, media_type=media_type_list[i],
                                         media_content=media_url)
            setting_media.save()
            i = i + 1

        j = 0
        for setting_title in setting_title_list:
            setting_title = SettingLang(title=setting_title, keywords=setting_keywords_list[j],
                                        about=setting_about_list[j], address=setting_address_list[j]
                                        , lang=setting_lang_list[j], company=setting_company_list[j],
                                        setting_id=setting_obj)

            setting_title.save()
            j = j + 1
        # return HttpResponse("OK")
        return render(request, 'setting.html')



