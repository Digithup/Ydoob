from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.files.storage import FileSystemStorage
from django.forms import modelformset_factory
from django.http import request, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from catalog.forms.forms import ProductsForm, ProductMediaForm
from catalog.models.models import Categories, Products, ProductMedia, ProductTransaction
from catalog.models.product_options import Filters
from core.forms.setting import SettingForm, SettingLangForm, SettingTagForm
from core.models.setting import Setting, SettingLang, SettingTags
from localization.models import Language

User = get_user_model()

def ProductAddopencart(request):
    filter = Filters.objects.all()
    # 'extra' means the number of photos that you can upload   ^
    if request.method == "POST":

        print(request)
        product_form = ProductsForm(request.POST or None, request.FILES or None)
        media_form = ProductMediaForm(request.POST or None, request.FILES or None)

        if product_form.is_valid() and media_form.is_valid():
            print(request.POST)
            product_created = True
            seller = request.user.id
            category = product_form.cleaned_data['category']
            title = product_form.cleaned_data['title']
            long_desc = product_form.cleaned_data['long_desc']
            keyword = product_form.cleaned_data['keyword']
            model = product_form.cleaned_data['model']
            brand = product_form.cleaned_data['brand']
            price = product_form.cleaned_data['price']
            quantity = product_form.cleaned_data['quantity']
            out_of_stock_status = product_form.cleaned_data['out_of_stock_status']
            requires_shipping = product_form.cleaned_data['requires_shipping']
            weight = product_form.cleaned_data['weight']
            length = product_form.cleaned_data['length']
            status = product_form.cleaned_data['status']
            slug = product_form.cleaned_data['slug']
            media_content_list = request.FILES.getlist("image")

            category = Categories.objects.get(title=category)
            seller = User.objects.get(id=seller)

            product_form = None

            if not product_form:

                print(request)
                print(request.POST)

                product_form = Products(seller=seller, category=category, title=title,
                                        long_desc=long_desc,
                                        model=model, brand=brand, price=price, quantity=quantity,
                                        out_of_stock_status=out_of_stock_status, keyword=keyword,

                                        requires_shipping=requires_shipping, weight=weight, length=length,
                                        status=status,
                                        slug=slug)

                product_form.save()
                i = 0

                for image in media_content_list:
                    media_form = ProductMedia(product=product_form,
                                              Image=image)
                    media_form.save()
                    i = i + 1
                    print(request.POST)
                    # use django messages framework
                messages.success(request,
                                 "Yeeew, check it out on the home page!")

                return HttpResponseRedirect("/admin/products/")

            else:
                print("Form invalid, see below error msg")
                print(request.POST)
                messages.error(request, "Error")

    else:

        product_form = ProductsForm()

        media_form = ProductMediaForm()
        # return redirect(reverse('core:ProductAdd'))

    return render(request, 'catalog/product/trushtest.html',
                  {'product_form': product_form, 'media_form': media_form ,'filters':filter,})

    # return HttpResponse("OK")
    # return redirect(reverse('vendors:ProductsList'))





class NewModelViewTest(View):
    def get(self, request, *args, **kwargs):
        print(request)
        setting_form = SettingForm()
        lang_form = SettingLangForm()
        tags_form = SettingTagForm()
        lang_list = Language.objects.filter(status=True)
        return render(request, 'setting/add-setting.html',
                      {"lang_list": lang_list, "setting_form": setting_form, "lang_form": lang_form,
                       "tags_form": tags_form})

    print(request)


def AddSetting(request):
    lang_list = Language.objects.filter(status=True)
    # 'extra' means the number of photos that you can upload   ^
    if request.method == "POST":

        print(request)
        setting_form = SettingForm(request.POST or None, request.FILES or None)
        lang_form = SettingLangForm(request.POST or None, request.FILES or None)
        tags_form = SettingTagForm(request.POST or None, request.FILES or None)

        if setting_form.is_valid() and tags_form.is_valid():
            print(request.POST)
            product_created = True

            phone = setting_form.cleaned_data['phone']
            email = setting_form.cleaned_data['email']
            image = setting_form.cleaned_data['image']
            facebook = setting_form.cleaned_data['facebook']
            instagram = setting_form.cleaned_data['instagram']
            twitter = setting_form.cleaned_data['twitter']
            youtube = setting_form.cleaned_data['youtube']
            status = setting_form.cleaned_data['status']
            slug = setting_form.cleaned_data['slug']

            setting = request.POST.get('setting_id')
            setting_lang_list = request.POST.getlist('lang[]')
            setting_title_list = request.POST.getlist('title[]')
            setting_keywords_list = request.POST.getlist('keywords[]')
            setting_company_list = request.POST.getlist('company[]')
            setting_address_list = request.POST.getlist('address[]')
            setting_about_list = request.POST.getlist('about[]')
            meta_title = tags_form.cleaned_data['meta_title']
            meta_description = tags_form.cleaned_data['meta_description']
            meta_keywords = tags_form.cleaned_data['meta_keywords']
            tags = tags_form.cleaned_data['tags']

            if not setting:

                print(request)
                print(request.POST)

                setting_form = Setting(phone=phone, email=email, image=image, facebook=facebook,
                                       instagram=instagram, twitter=twitter, youtube=youtube,
                                       status=status, slug=slug)

                setting_form.save()

                j = 0
                for setting_title in setting_title_list:
                    lang_form = SettingLang(title=setting_title, keywords=setting_keywords_list[j],
                                            about=setting_about_list[j], address=setting_address_list[j]
                                            , lang=setting_lang_list[j], company=setting_company_list[j],
                                            setting=setting_form)

                    lang_form.save()
                    j = j + 1

                tags_form = SettingTags(setting=setting_form, meta_title=meta_title,
                                        meta_description=meta_description,
                                        meta_keywords=meta_keywords, tags=tags)
                tags_form.save()

                print(request.POST)
                # use django messages framework
                messages.success(request,
                                 "Yeeew, check it out on the home page!")

                return HttpResponseRedirect("/dashboard/setting/")

            else:
                print("Form invalid, see below error msg")
                print(request.POST)
                messages.error(request, "Error")

    else:

        setting_form = SettingForm()
        lang_form = SettingLangForm()
        tags_form = SettingTagForm()
        # return redirect(reverse('core:ProductAdd'))

    return render(request, 'setting/add-setting.html',
                  {"lang_list": lang_list, 'setting_form': setting_form, 'lang_form': lang_form,
                   'tags_form': tags_form})

    # return HttpResponse("OK")
    # return redirect(reverse('vendors:ProductsList'))


class UpdateSetting(View):

    def get(self, request,slug, *args, **kwargs):

        setting = Setting.objects.get(slug=slug)
        setting_lang = SettingLang.objects.filter(setting=setting, lang=request.LANGUAGE_CODE)
        setting_tag = SettingTags.objects.get(setting=setting)
        lang_list = Language.objects.filter(status=True)
        setting_form = SettingForm()
        lang_form = SettingLangForm()
        tags_form = SettingTagForm()
        return render(request, "setting/update-setting.html",
                      {"setting": setting, "setting_lang": setting_lang,
                       "setting_tag": setting_tag, "lang_list": lang_list ,"setting_form":setting_form})

    def post(self, request,slug, *args, **kwargs):

        if request.method == "POST":
            print(request)
            setting_form = SettingForm(request.POST or None, request.FILES or None)
            lang_form = SettingLangForm(request.POST or None, request.FILES or None)
            tags_form = SettingTagForm(request.POST or None, request.FILES or None)

            if setting_form.is_valid() and tags_form.is_valid():
                print(request.POST)
                product_created = True

                phone = setting_form.cleaned_data['phone']
                email = setting_form.cleaned_data['email']
                image = setting_form.cleaned_data['image']
                facebook = setting_form.cleaned_data['facebook']
                instagram = setting_form.cleaned_data['instagram']
                twitter = setting_form.cleaned_data['twitter']
                youtube = setting_form.cleaned_data['youtube']
                status = setting_form.cleaned_data['status']
                slugy = setting_form.cleaned_data['slug']

                setting = Setting.objects.get(slug=slug)
                setting_lang_list = request.POST.getlist('lang[]')
                setting_title_list = request.POST.getlist('title[]')
                setting_keywords_list = request.POST.getlist('keywords[]')
                setting_company_list = request.POST.getlist('company[]')
                setting_address_list = request.POST.getlist('address[]')
                setting_about_list = request.POST.getlist('about[]')
                meta_title = tags_form.cleaned_data['meta_title']
                meta_description = tags_form.cleaned_data['meta_description']
                meta_keywords = tags_form.cleaned_data['meta_keywords']
                tags = tags_form.cleaned_data['tags']

                if setting:
                    setting.phone = phone
                    setting.email = email
                    setting.image = image
                    setting.facebook = facebook
                    setting.instagram = instagram
                    setting.twitter = twitter
                    setting.youtube = youtube
                    setting.status = status
                    setting.slug = slugy
                    setting.save()

                    print(request)
                    print(request.POST)
                    setting_lang = SettingLang.objects.filter(setting=setting, ).delete()
                    setting_tag = SettingTags.objects.filter(setting=setting).delete()

                    j = 0
                    for setting_title in setting_title_list:
                        setting_lang = SettingLang(title=setting_title, keywords=setting_keywords_list[j],
                                                about=setting_about_list[j], address=setting_address_list[j]
                                                , lang=setting_lang_list[j], company=setting_company_list[j],
                                                setting=setting)

                        setting_lang.save()
                        j = j + 1


                    setting_tag = SettingTags(setting=setting, meta_title=meta_title,
                                            meta_description=meta_description,
                                            meta_keywords=meta_keywords, tags=tags)
                    setting_tag.save()

                    print(request.POST)
                    # use django messages framework
                    messages.success(request,
                                     "Yeeew, check it out on the home page!")

                    return HttpResponseRedirect("/admin/setting/")

                else:
                    print("Form invalid, see below error msg")
                    print(request.POST)
                    messages.error(request, "Error")

        else:

            setting_form = SettingForm()
            lang_form = SettingLangForm()
            tags_form = SettingTagForm()

            # return redirect(reverse('core:ProductAdd'))

        return render(request, 'setting/update-setting.html',
                      {'setting_form': setting_form, 'lang_form': lang_form,
                       'tags_form': tags_form})

        # return HttpResponse("OK")
        # return redirect(reverse('vendors:ProductsList'))


"""

def banner_create(request):
    qs = Slider.objects.none()
    BannersFormSet = modelformset_factory(Slider, form=BannerAddForm, exclude=['groups', 'status'], extra=1,
                                          can_delete=True)

    if request.method == 'POST':
        banner_form = BannerAddForm(request.POST, prefix='design')

        formset = BannersFormSet(request.POST, request.FILES)

        if formset.is_valid() and banner_form.is_valid():
            # Generate a workday object
            banner = banner_form.save(commit=False)
            banner.groups = banner_form.cleaned_data['groups']
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
                                     e.banner.groups +
                                     ": " + e.caption + " (" + str(e.groups) + ") - "
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

            setting_media = Setting(setting_id=setting_obj, media_type=media_type_list[i],
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
        return render(request, 'setting/add-setting.html')


# https://stackoverflow.com/questions/569468/django-multiple-models-in-one-template-using-forms

class ProductCreateTest2(View):
    def get(self, request, *args, **kwargs):
        category = Categories.objects.filter(status=True)
        sellers = request.user.id

        return render(request, "catalog/product/add-product.html", {"categories": category, "sellers": sellers})

        # return render(request, "vendor/catalog/product/add-product.html", {"categories": category, "sellers": sellers})

    print(request)

    def post(self, request, *args, **kwargs):
        seller = request.POST.get("seller")
        category = request.POST.get("category")
        title = request.POST.get("title")
        long_desc = request.POST.get("long_desc")
        keyword = request.POST.get("keyword")
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
        image = request.POST.getlist("image")
        media_type_list = request.POST.getlist("media_type[]")
        media_content_list = request.FILES.getlist("media_content[]")
        product_tags = request.POST.get("product_tags")
        category = Categories.objects.get(id=category)
        seller = User.objects.get(id=seller)
        print(request.POST)
        if title == '' or slug == "":
            messages.error(request, ['please fill'])
            category = Categories.objects.filter(status=True)
            sellers = request.user.id

            return render(request, "catalog/product/add-product.html", {"categories": category, "sellers": sellers})
        else:

            product = Products(seller=seller, category=category, title=title, long_desc=long_desc,
                               model=model, brand=brand, price=price, quantity=quantity,
                               out_of_stock_status=out_of_stock_status, keyword=keyword, image=image,
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

        product_transaction = ProductTransaction(product_id=product, transaction_type=1,
                                                 transaction_product_count=quantity,
                                                 transaction_description="Initially Item Added in Stocks")
        print(request.POST)
        product_transaction.save()
        return HttpResponse("OK")
        # return redirect(reverse('vendors:ProductsList'))


#################################################################
####################################
#####################


class ProductCreateTestNe(View):

    def get(self, request, *args, **kwargs):
        product_form = ProductsForm()
        ImageFormSet = modelformset_factory(ProductMedia,
                                            form=ProductMediaForm, extra=6)
        formset = ImageFormSet(queryset=ProductMedia.objects.none())
        category = Categories.objects.filter(status=True)
        sellers = request.user.id
        print(request)
        return render(request, 'catalog/product/addnew.html',
                      {"categories": category, "sellers": sellers, 'product_form': product_form,
                       'formset': formset, })

    def post(self, request, *args, **kwargs):
        ImageFormSet = modelformset_factory(ProductMedia,
                                            form=ProductMediaForm, extra=6)
        # 'extra' means the number of photos that you can upload   ^
        if request.method == "POST":

            print(request)
            product_form = ProductsForm(request.POST or None, request.FILES or None)
            formset = ImageFormSet(request.POST, request.FILES,
                                   queryset=ProductMedia.objects.none())
            if product_form.is_valid() and formset.is_valid():
                print(request.POST)
                product_created = True
                seller = product_form.cleaned_data['seller']
                category = product_form.cleaned_data['category']
                title = product_form.cleaned_data['title']
                long_desc = product_form.cleaned_data['long_desc']
                keyword = product_form.cleaned_data['keyword']
                model = product_form.cleaned_data['model']
                brand = product_form.cleaned_data['brand']
                price = product_form.cleaned_data['price']
                quantity = product_form.cleaned_data['quantity']
                out_of_stock_status = product_form.cleaned_data['out_of_stock_status']
                requires_shipping = product_form.cleaned_data['requires_shipping']
                weight = product_form.cleaned_data['weight']
                length = product_form.cleaned_data['length']
                status = product_form.cleaned_data['status']
                slug = product_form.cleaned_data['slug']

                category = Categories.objects.get(title=category)
                seller = User.objects.get(email=seller)
                product = None
                product_obj = None

                if not product:
                    print(request)
                print(request.POST)

                product_obj = Products.objects.create(seller=seller, category=category, title=title,
                                                      long_desc=long_desc,
                                                      model=model, brand=brand, price=price, quantity=quantity,
                                                      out_of_stock_status=out_of_stock_status, keyword=keyword,

                                                      requires_shipping=requires_shipping, weight=weight, length=length,
                                                      status=status,
                                                      slug=slug)

                print(request.POST)
                product_obj.seller = seller
                product_obj.category = category
                product_obj.title = title
                product_obj.long_desc = long_desc
                product_obj.model = model
                product_obj.brand = brand
                product_obj.price = price
                product_obj.quantity = quantity
                product_obj.out_of_stock_status = out_of_stock_status
                product_obj.keyword = keyword

                product_obj.requires_shipping = requires_shipping
                product_obj.weight = weight
                product_obj.length = length
                product_obj.status = status
                product_obj.slug = slug

                messages.success(request, "SUCCESS")
                product_obj.save()

                for form in formset.cleaned_data:
                    # this helps to not crash if the user
                    # do not upload all the photos
                    if form:
                        media_content = form['media_content']
                        photo = ProductMedia(product=product_obj, media_content=media_content)
                        photo.save()
                    # use django messages framework
                messages.success(request,
                                 "Yeeew, check it out on the home page!")
                return HttpResponseRedirect('/')
                return HttpResponse("wrong")
                # return HttpResponseRedirect("/admin/products/Products_list")

            else:
                print("Form invalid, see below error msg")
                print(request.POST)
                print(product_form.errors, formset.errors)
                messages.error(request, "Error")

        else:

            product_form = ProductsForm()
            formset = ImageFormSet(queryset=ProductMedia.objects.none())
            # media_form = ProductMediaForm()
            return HttpResponse("OK")

            # return render(request, 'catalog/product/addnew.html', {'product_form': product_form, 'formset': formset, })

            # return HttpResponse("OK")
            # return redirect(reverse('vendors:ProductsList'))


def ProductCreateTestNew(self, request, *args, **kwargs):
    # 'extra' means the number of photos that you can upload   ^
    if request.method == "POST":

        print(request)
        product_form = ProductsForm(request.POST or None, request.FILES or None)
        media_form = ProductMediaForm(request.POST or None, request.FILES or None)

        if product_form.is_valid() and media_form.is_valid():
            print(request.POST)
            product_created = True
            seller = request.user.id
            category = product_form.cleaned_data['category']
            title = product_form.cleaned_data['title']
            long_desc = product_form.cleaned_data['long_desc']
            keyword = product_form.cleaned_data['keyword']
            model = product_form.cleaned_data['model']
            brand = product_form.cleaned_data['brand']
            price = product_form.cleaned_data['price']
            quantity = product_form.cleaned_data['quantity']
            out_of_stock_status = product_form.cleaned_data['out_of_stock_status']
            requires_shipping = product_form.cleaned_data['requires_shipping']
            weight = product_form.cleaned_data['weight']
            length = product_form.cleaned_data['length']
            status = product_form.cleaned_data['status']
            slug = product_form.cleaned_data['slug']
            media_content_list = request.FILES.getlist("image")

            category = Categories.objects.get(title=category)
            seller = User.objects.get(id=seller)

            product_form = None

            if not product_form:

                print(request)
                print(request.POST)

                product_form = Products(seller=seller, category=category, title=title,
                                        long_desc=long_desc,
                                        model=model, brand=brand, price=price, quantity=quantity,
                                        out_of_stock_status=out_of_stock_status, keyword=keyword,

                                        requires_shipping=requires_shipping, weight=weight, length=length,
                                        status=status,
                                        slug=slug)

                product_form.save()
                i = 0

                for image in media_content_list:
                    media_form = ProductMedia(product=product_form,
                                              Image=image)
                    media_form.save()
                    i = i + 1
                    print(request.POST)
                    # use django messages framework
                messages.success(request,
                                 "Yeeew, check it out on the home page!")

                return HttpResponseRedirect("/admin/products/Products_list")

            else:
                print("Form invalid, see below error msg")
                print(request.POST)
                messages.error(request, "Error")

    else:

        product_form = ProductsForm()

        media_form = ProductMediaForm()
        # return redirect(reverse('core:ProductAdd'))

    return render(request, 'catalog/product/add-producttest.html',
                  {'product_form': product_form, 'media_form': media_form})

    # return HttpResponse("OK")
    # return redirect(reverse('vendors:ProductsList'))
