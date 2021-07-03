from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.forms import modelformset_factory
from django.http import request, HttpResponse
from django.shortcuts import redirect
from django.views import View

from core.forms.banners_forms import BannerAddForm, render
from core.models.design import Slider
from core.models.setting import Setting, SettingLang, SettingMedia
from localization.models import Language


def banner_create(request):
    qs = Slider.objects.none()
    BannersFormSet = modelformset_factory(Slider, form=BannerAddForm, exclude=['group', 'status'], extra=1,
                                          can_delete=True)

    if request.method == 'POST':
        banner_form = BannerAddForm(request.POST, prefix='banner')

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
            banner_form = BannerAddForm(request.POST, prefix='banner')
            formset = BannersFormSet(request.POST, request.FILES)

            for dict in formset.errors:
                messages.add_message(request, messages.ERROR, dict)

            context = {
                'banner_form': banner_form,
                'formset': formset,
            }
            return render(request, 'banner/add-banner.html', context)

    else:
        banner_form = BannerAddForm(prefix='banner')
        formset = BannersFormSet(queryset=qs)
        context = {
            'banner_form': banner_form,
            'formset': formset,
        }
        return render(request, 'banner/add-banner.html', context)


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

        #status = request.POST.get("status")

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
        #return HttpResponse("OK")
        return render(request, 'setting.html')
