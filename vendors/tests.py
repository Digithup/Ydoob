import os
import uuid

from PIL import Image
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.test import TestCase

# Create your tests here.
from django.urls import reverse, reverse_lazy
from django.utils.html import format_html
from django.views import View
from django.views.generic import ListView
from requests import request
from accounts.models import User
from vendors.models import Store, StoreMedia


def clean(self):
    lockup = {}

    unique_togethers = self._meta.unique_together[0]  # these could throw an error

    for field in unique_togethers:
        f = self._meta.get_field(field)

        value = getattr(self, f.attname)

        if value is None:
            continue

        if f.primary_key and not self._state.adding:
            continue

        lockup[str(field)] = value

    qs = Store.objects.filter(**lockup)

    if qs.exists and self._state.adding:
        raise ValidationError(
            format_html('''this object already exist plese edit it on <a href="{}">Edit</a>''',
                        reverse('admin:testing_snippet_change', args=(qs[0].pk,))))


class CreateStoreTest(View):
    def get(self, request, *args, **kwargs):
        print(request)
        # vendor = Store.objects.get_or_create()
        # seller = request.user

        return render(request, "store-page/create-store.html", )

    print(request)

    def post(self, request, *args, **kwargs):
        title_group = request.POST.get("title")
        address = request.POST.get("address")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        vendor_id = request.user.id
        print(request.POST)
        vendor = User.objects.filter(seller=True)
        status = Store.objects.filter(status='Disable')

        if vendor and status:
            messages.error(request,
                           format_html('''You already have a store wait for activate &nbsp; &nbsp;  or learn how to sell &nbsp; 
                <a href=""> Edit</a> ''',
                                       reverse('home:index', )))

            return render(request, "store-page/create-store.html", )

        else:
            store = Store(title=title_group, address=address, phone=phone, email=email, vendor_id=vendor_id)
            store.save()
            # return HttpResponse("OK")
            return render(request, 'store-page/create-success.html', )
            # return HttpResponseRedirect(reverse_lazy('home:index'))


"""
def become_sellers(request, id):
    forms = StoreAddForm
    if request.method == 'POST':

        print(request.POST)
        forms = StoreAddForm(request.POST, request.FILES)
        if forms.is_valid():
            store = forms.save(commit=False)
            store.vendor = request.user
            store.save()
            # Add this to check if the email already exists in your database or not
            # store.save()
            return render(request, 'store-page/create-success.html', )
    else:
        forms = StoreAddForm(request.POST, request.FILES)
        return render(request, 'store-page/create-store.html', {'forms': forms})
    return render(request, 'store-page/create-store.html', {'forms': forms})


@login_required
def ajax_avatar_upload(request):
    user = request.user
    user_profile = get_object_or_404(UserProfile, user=user)

    if request.method == "POST":
        form = AvatarUploadForm(request.POST, request.FILES)
        if form.is_valid():
            img = request.FILES['avatar_file']  # Get upload pictures
            cropped_avatar = crop_image(img, user.id)
            user_profile.avatar = cropped_avatar  # The path to the image changes to the current membership database
         user_profile.save()
    return HttpResponseRedirect(reverse('myaccount:profile'))
"""


def crop_image(file, uid):
    # Randomly generated new image name, custom path.
    ext = file.name.split('.')[-1]
    file_name = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    cropped_avatar = os.path.join(uid, "avatar", file_name)
    # Relative root directory path

    file_path = os.path.join("media", uid, "avatar", file_name)

    # Crop picture,With compact dimensions200*200。
    img = Image.open(file)
    crop_im = img.crop((50, 50, 300, 300)).resize((200, 200), Image.ANTIALIAS)
    crop_im.save(file_path)

    return cropped_avatar


class EditStoreTestt(View):

    def get(self, request, *args, **kwargs, ):
        store_id = kwargs["store_id"]
        stores = Store.objects.get(id=store_id)
        store_media = StoreMedia.objects.filter(store_id=store_id)

        return render(request, "vendor/vendor-edit-store-profile.html",
                      {"stores": stores, "store_media": store_media, })

    def post(self, request, *args, **kwargs):
        store_id = kwargs["store_id"]
        stores = Store.objects.get(id=store_id)
        title = request.POST.get("title")
        phone = request.POST.get("phone")
        company = request.POST.get("company")
        media_type_list = request.POST.getlist("media_type[]")
        media_content_list = request.POST.getlist("media_content_list[]")
        media_content_ids = request.POST.getlist("media_content_id[]")
        about = request.POST.get("about")
        keywords = request.POST.get("keywords")
        slug = request.POST.get("slug")
        country = request.POST.get("country")
        city = request.POST.get("city")
        address = request.POST.get("address")
        facebook = request.POST.get("facebook")
        instagram = request.POST.get("instagram")
        twitter = request.POST.get("twitter")
        youtube = request.POST.get("youtube")
        print(request.POST)
        # status = request.POST.get("status")
        seller = request.user.id
        vendor = User.objects.get(id=seller)

        # vendor = seller
        # vendor =Store.objects.get(vendor=owner)
        # vendor_id = Store.objects.filter(vendor_id=request.user.id)

        store_obj = Store(title=title, phone=phone, company=company, about=about,
                          keywords=keywords, slug=slug, country=country, city=city, address=address,
                          facebook=facebook, instagram=instagram, twitter=twitter, youtube=youtube, vendor=vendor)
        store_obj.save()

        i = 0
        for media_content in media_content_list:
            fs = FileSystemStorage()
            filename = fs.save(media_content.name, media_content)
            media_url = fs.url(filename)
            media_content_id = media_content_ids[i]
            if media_content_id == "blank" and media_content != "":
                store_media = StoreMedia(store_id=store_obj, media_type=media_type_list[i], media_content=media_url)
                store_media.save()
            else:
                if media_content != "":
                    store_media = StoreMedia.objects.get(id=media_content_id)
                    store_media.media_content = media_content
                    store_media.store_id = store_obj
                    store_media.save()

            i = i + 1

            print(request.POST)
            print(request)
            messages.error(request, "Error")

        return HttpResponse("OK")

        # return HttpResponseRedirect(reverse_lazy('vendors:VendorDashboard' ))


class EditStoreTest(View):

    def get(self, request, *args, **kwargs, ):
        store_id = kwargs["store_id"]

        stores = Store.objects.get(id=store_id)
        store_medias = StoreMedia.objects.get(store_id=store_id)
        #media_id = kwargs["store_medias"]
        #media_store = StoreMedia.objects.filter(id=media_id)

        return render(request, "vendor/vendor-edit-store-profile.html",
                      {"stores": stores, 'store_medias': store_medias })

    def post(self, request, *args, **kwargs):
        title = request.POST.get("title")
        phone = request.POST.get("phone")
        company = request.POST.get("company")
        media_type_list = request.POST.getlist("media_type[]")
        media_content_list = request.FILES.getlist("media_content[]")
        media_content_ids = request.POST.getlist("media_content_id[]")
        about = request.POST.get("about")
        keywords = request.POST.get("keywords")
        slug = request.POST.get("slug")
        country = request.POST.get("country")
        city = request.POST.get("city")
        address = request.POST.get("address")
        facebook = request.POST.get("facebook")
        instagram = request.POST.get("instagram")
        twitter = request.POST.get("twitter")
        youtube = request.POST.get("youtube")
        print(request.POST)
        # status = request.POST.get("status")

        store_id = kwargs["store_id"]
        # vendor = User.objects.get(id=User.id)
        vendor = request.user.id

        store_id = kwargs["store_id"]
        store = Store.objects.get(id=store_id)
        # store.vendor=stores
        store.title = title
        store.phone = phone
        store.company = company
        store.about = about
        store.keywords = keywords
        store.slug = slug
        store.country = country
        store.city = city
        store.address = address
        store.facebook = facebook
        store.instagram = instagram
        store.twitter = twitter
        store.youtube = youtube

        store.save()
        i = 0
        for media_content in media_content_list:
            fs = FileSystemStorage()
            filename = fs.save(media_content.name, media_content)
            media_url = fs.url(filename)
            media_content_id = media_content_ids[i]
            if media_content_id == "blank" and media_content != "":
                store_media = StoreMedia(store_id=store_id, media_type=media_type_list[i], media_content=media_url)
                store_media.save()
            else:
                if media_content != "":
                    store_media = StoreMedia.objects.get(id=media_content_id)
                    store_media.media_content = media_content
                    #store_media.store_id = store.id
                    store_media.save()

            i = i + 1

            print(request.POST)
            print(request)
            messages.error(request, "Error")

        return HttpResponse("OK")

        # return HttpResponseRedirect(reverse_lazy('vendors:VendorDashboard' ))
