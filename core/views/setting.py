from pyexpat import model

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DeleteView, UpdateView, CreateView

from core.decorators import allowed_users
from core.forms.setting import SettingLangForm, SettingForm, SiteForm
from core.models.setting import Setting, SettingLang



# Create your views here.
from localization.models.models import Language
from sales.forms.order import PaymentMethodsForm
from sales.models.orders import PaymentMethods


class AdminSetting(ListView):
    model = Setting

    template_name = 'setting/admin-setting.html'

@login_required(login_url='/login')
@allowed_users(allowed_roles=['admin'])
def setting(request):
    setting = Setting.objects.first()
    setting_lang = SettingLang.objects.first()
    context = {'setting': setting,
               'setting_lang': setting_lang,

               }

    def get_object(self, queryset=None):
        if "pk" not in self.kwargs:
            self.kwargs['pk'] = None
        obj, created = Setting.objects.get_or_create(pk=self.kwargs.get('id', None),
                                                     )

        return obj

    return render(request, 'setting.html', context)

@login_required(login_url='/login')
@allowed_users(allowed_roles=['admin'])
def add_setting(request):

    langlist = Language.objects.filter(status=True)
    if request.method == "POST":
        # langlist=Language.objects.filter(status=True)

        print(request.POST)
        setting_created = True
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
        if not setting_id:
            print(request.POST)
            setting_obj = Setting.objects.create(email=email, phone=phone,
                                                 facebook=facebook, instagram=instagram,
                                                 twitter=twitter, youtube=youtube, status=status,
                                                 )  # create will create as well as save too in db.


        else:
            # handling all cases of the tags
            print(request.POST)
            setting_obj = Setting.objects.get(id=setting_id)
            setting_created = False

        i = 0

        for media_content in media_content_list:
            fs = FileSystemStorage()
            filename = fs.save(media_content.name, media_content)
            media_url = fs.url(filename)

            setting_media = Setting(setting_id=setting_obj, media_type=media_type_list[i],
                                         media_content=media_url)
            setting_media.save()
            i = i + 1


        j =0
        for setting_title in setting_title_list:
            setting_title = SettingLang(title=setting_title,keywords=setting_keywords_list[j],
                                        about=setting_about_list[j], address=setting_address_list[j]
                                        ,lang=setting_lang_list[j],company=setting_company_list[j],
                                                                    setting_id=setting_obj)

            setting_title.save()
            j = j + 1



        setting_obj.email = email
        setting_obj.phone = phone
        setting_obj.facebook = facebook
        setting_obj.instagram = instagram
        setting_obj.twitter = twitter
        setting_obj.youtube = youtube
        setting_obj.status = status
        print(request.POST)
        setting_obj.save()  # last_modified field won't update on chaning other model field, save() trigger change
        # return reverse('core:catalog')
        return HttpResponseRedirect('/admin/setting/add', setting_created)
        # return render(request,template_name='admin/pages/vendor-products.html')
        # return getNoteResponseData(product_obj, tags, product_created)
    else:
        print("Form invalid, see below error msg")
        print(request.POST)

        messages.error(request, "Error")
    # if GET method form, or anything wrong then we will create blank form

    # return HttpResponseRedirect('/')
    return render(request, 'setting/add-setting.html', {'langlist': langlist})

@login_required(login_url='/login')
@allowed_users(allowed_roles=['admin'])
def update_setting(request):
    lang = Language.objects.all()
    try:
        setting = Setting.objects.first()
        lang_setting = SettingLang.objects.first()
        forms = SettingForm(instance=setting)
        lang_form = SettingLangForm
        if request.method == 'POST':
            forms = SettingForm(request.POST, request.FILES, instance=setting)
            lang_form = SettingLangForm(request.POST)
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

    forms = SettingForm(instance=setting)
    lang_form = SettingLangForm
    if request.method == 'POST':
        forms = SettingForm(request.POST, request.FILES, instance=setting)
        lang_form = SettingLangForm(request.POST)
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


class SettingDelete(DeleteView):
    model = Setting
    fields = '__all__'
    success_url = reverse_lazy('core:AdminSetting')
    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def dispatch(self, *args, **kwargs):
        return super(SettingDelete, self).dispatch(*args, **kwargs)


class AdminSite(ListView):
    model = Site
    template_name = 'setting/site/admin-site.html'


class AdminSiteUpdate(UpdateView):
    model=Site
    form_class=SiteForm
    template_name = 'setting/site/update-site.html'
    success_url = reverse_lazy('core:AdminSite')

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def dispatch(self, *args, **kwargs):
        return super(AdminSiteUpdate, self).dispatch(*args, **kwargs)

class PaymentMethodsList(ListView):
    model = PaymentMethods
    template_name = 'setting/PaymentMethods/admin-PaymentMethods.html'


class PaymentMethodsCreate(CreateView):
    model = PaymentMethods
    #fields = '__all__'
    form_class = PaymentMethodsForm
    template_name = 'setting/PaymentMethods/add-PaymentMethods.html'
    success_url = reverse_lazy('core:PaymentMethodsList')

    # @method_decorator(allowed_users(allowed_roles=['admin']))
    # def dispatch(self, *args, **kwargs):
    #     return super(PaymentMethodsCreate, self).dispatch(*args, **kwargs)


class PaymentMethodsUpdate(UpdateView):
    model=PaymentMethods
    fields = '__all__'
    template_name = 'setting/PaymentMethods/update-PaymentMethods.html'
    success_url = reverse_lazy('core:PaymentMethodsList')

    @method_decorator(allowed_users(allowed_roles=['admin']))
    def dispatch(self, *args, **kwargs):
        return super(PaymentMethodsUpdate, self).dispatch(*args, **kwargs)

class PaymentMethodsDelete(DeleteView):
    model = PaymentMethods
    fields = '__all__'
    success_url = reverse_lazy('core:PaymentMethodsList')

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)