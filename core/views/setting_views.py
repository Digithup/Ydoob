from django.contrib import messages
from django.forms import formset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from core.forms.seeting_forms import SettingAddForm, SettingLangAddForm
from core.models.models import Setting, SettingLang
from localization.models import Language


def setting(request):
    set = Setting.objects.all()
    setting_lang = SettingLang.objects.first()
    context = {'set': set,
               'setting_lang': setting_lang,

               }

    def get_object(self, queryset=None):
        if "pk" not in self.kwargs:
            self.kwargs['pk'] = None
        obj, created = Setting.objects.get_or_create(pk=self.kwargs.get('id', None),
                                                     )

        return obj

    return render(request, 'setting.html', context)


def add_setting(request):
    langlist = Language.objects.filter(status=True)
    if request.method == "POST":
        langlist = Language.objects.filter(status=True)
        form = SettingAddForm(request.POST or None, request.FILES or None)
        lang_form = SettingLangAddForm(request.POST or None, request.FILES or None)
        files = request.FILES.getlist('images')
        print(request.POST)
        if form.is_valid() and lang_form.is_valid():
            print(request.POST)
            setting_created = True
            title = request.POST.getlist("title[]")
            keywords = request.POST.getlist("keywords[]")
            about = request.POST.getlist("about[]")
            company = request.POST.getlist("company[]")
            contact = request.POST.getlist("contact[]")
            address = request.POST.getlist("address[]")
            slug = request.POST.get("slug")
            email = request.POST.get['email']
            phone = request.POST.get['phone']
            image = request.FILES.get('image')
            facebook = request.POST.get['facebook']
            instagram = form.cleaned_data['instagram']
            twitter = form.cleaned_data['twitter']
            youtube = form.cleaned_data['youtube']
            status = form.cleaned_data['status']
            setting_id = form.cleaned_data['setting_id']
            if not setting_id:
                print(request.POST)
                setting = Setting.objects.create(email=email, phone=phone,
                                                 facebook=facebook, instagram=instagram,
                                                 twitter=twitter, youtube=youtube, image=image, status=status,
                                                 slug=slug,
                                                 setting_id=setting_id
                                                 )  # create will create as well as save too in db.
                setting.save()
                i = 0
                # for i in langlist():
                # lang_obj, created = SettingLang.objects.get_or_create(name=i)
                # lang_obj.title = i.title
                # setting_obj.SettingLang.add(lang_obj)  # it won't add duplicated as stated in django docs

                for title_list in title:
                    setting_title = SettingLang(title=title_list, title_details=title[i], setting_id=setting)
                    setting_title.save()

                for keywords_list in keywords:
                    setting_keywords = SettingLang(keywords=keywords_list, keywords_details=keywords[i],
                                                   setting_id=setting)
                    setting_keywords.save()

                for about_list in about:
                    setting_about = SettingLang(about=about_list, about_details=about[i], setting_id=setting)
                    setting_about.save()

                for company_list in company:
                    setting_company = SettingLang(company=company_list, company_details=title[i], setting_id=setting)
                    setting_company.save()

                for contact_list in contact:
                    setting_contact = SettingLang(title=contact_list, contact_details=contact[i], setting_id=setting)
                    setting_contact.save()

                for address_list in title:
                    setting_address = SettingLang(address=address_list, address_details=address[i], setting_id=setting)
                    setting_address.save()

                for slug_list in slug:
                    setting_slug = SettingLang(slug=slug_list, slug_details=slug[i], setting_id=setting)
                    setting_slug.save()


            else:
                # handling all cases of the tags
                print(request.POST)
                setting = Setting.objects.get(id=setting_id)
                setting_created = False
            setting.email = email
            setting.phone = phone
            setting.facebook = facebook
            setting.instagram = instagram
            setting.twitter = twitter
            setting.youtube = youtube
            setting.image = image
            setting.status = status
            setting.title = title
            setting.keywords = keywords
            setting.about = about
            setting.company = company
            setting.contact = contact
            setting.address = address

            print(request.POST)
            setting.save()  # last_modified field won't update on chaning other model field, save() trigger change
            # return reverse('core:catalog')
            return HttpResponseRedirect('/admin/', setting_created)
            # return render(request,template_name='admin/pages/Products-admin.html')
            # return getNoteResponseData(Products_obj, tags, Products_created)
        else:
            print("Form invalid, see below error msg")
            print(request.POST)
            print(form.errors)
            messages.error(request, "Error")
    # if GET method form, or anything wrong then we will create blank form
    else:

        form = SettingAddForm()
        lang_form = SettingLangAddForm()

    # return HttpResponseRedirect('/')
    return render(request, 'add-setting.html', {'form': form, 'lang_form': lang_form, 'langlist': langlist})


def update_setting(request):
    lang = Language.objects.all()
    try:
        setting = Setting.objects.first()
        lang_setting = SettingLang.objects.first()
        forms = SettingAddForm(instance=setting)
        lang_form = SettingLangAddForm
        if request.method == 'POST':
            forms = SettingAddForm(request.POST, request.FILES, instance=setting)
            lang_form = SettingLangAddForm(request.POST)
            if forms.is_valid() and lang_form.is_valid():
                lang_form.save(commit=False)
                forms.save(commit=False)

        context = {
            'lang': lang,
            'setting': setting,
            'lang_setting': lang_setting,
            'forms': forms,
            'lang_form': lang_form,
        }
        return render(request, 'setting.html', context)
    except Setting.DoesNotExist:
        setting = None

    forms = SettingAddForm(instance=setting)
    lang_form = SettingLangAddForm
    if request.method == 'POST':
        forms = SettingAddForm(request.POST, request.FILES, instance=setting)
        lang_form = SettingLangAddForm(request.POST)
        if forms.is_valid() and lang_form.is_valid():
            lang_form.save(commit=False)
            forms.save(commit=False)

    context = {
        'lang': lang,
        'setting': setting,
        'forms': forms,
        'lang_form': lang_form,
    }

    return render(request, 'setting.html', context)
