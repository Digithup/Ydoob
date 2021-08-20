from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import request, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, DetailView, DeleteView, CreateView

from core.forms.banner import BannersAddForm
from core.models.design import Slider, SliderGroup, SliderMedia, Banners


class SliderView(TemplateView):
    template_name = "design/slider/sliders-admin.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sliders'] = Slider.objects.all()
        return context


class SliderDetailView(DetailView):
    model = Slider
    context_object_name = 'slider'
    template_name = 'design/slider/slider-detail.html'


class SliderGroupCreate(CreateView):
    model = SliderGroup
    fields = '__all__'
    template_name = 'design/slider/add-slider-group.html'
    success_url = reverse_lazy('core:SliderView')


class SliderDelete(DeleteView):
    model = Slider
    fields = '__all__'
    success_url = reverse_lazy('core:SliderView')

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)


class SliderCreate(View):
    def get(self, request, *args, **kwargs):
        groups = SliderGroup.objects.filter(status=True)

        return render(request, "design/slider/slider-create.html",
                      {"groups": groups, })

    print(request)

    def post(self, request, *args, **kwargs):
        title = request.POST.get("title")
        group = request.POST.get("group")
        status = request.POST.get("status")
        sort_order = request.POST.get("sort_order")
        media_type_list = request.POST.getlist("media_type[]")
        media_content_list = request.FILES.getlist("media_content[]")
        media_link_list = request.POST.getlist("media_link[]")

        print(request.POST)

        # status = request.POST.get("status")

        group = SliderGroup.objects.get(id=group)

        slider = Slider(title=title, group=group, status=status, sort_order=sort_order,
                        )
        slider.save()

        i = 0
        for media_content in media_content_list:
            fs = FileSystemStorage()
            filename = fs.save(media_content.name, media_content)
            media_url = fs.url(filename)
            slider_media = SliderMedia(slider_id=slider, media_type=media_type_list[i],
                                       media_link=media_link_list[i], media_content=media_url)
            slider_media.save()
            i = i + 1

        # return HttpResponse("OK")
        return HttpResponseRedirect(reverse_lazy('core:SliderView'))


###################Banners#############

class BannersView(TemplateView):
    template_name = "design/banner/banners-admin.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['banners'] = Banners.objects.all()
        return context


class BannerDetailView(DetailView):
    model = Banners
    context_object_name = 'design'
    template_name = 'design/banner/banner-detail.html'


class BannerDelete(DeleteView):
    model = Banners
    fields = '__all__'
    success_url = reverse_lazy('core:BannerView')

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)


def BannerCreate(request):  # sourcery skip: aug-assign, convert-to-enumerate

    if request.method == "POST":
        print(request)

        banner_form = BannersAddForm(request.POST or None, request.FILES or None)

        if banner_form.is_valid():

            return _extracted_from_BannerCreate_10(request, banner_form)
        print("Form invalid, see below error msg")
        print(request.POST)
        messages.error(request, "Error")

    else:
        banner_form = BannersAddForm()
# return redirect(reverse('core:ProductAdd'))

    return render(request, 'design/banner/add-banner.html',
                  {'banner_form': banner_form, }
                  )

def _extracted_from_BannerCreate_10(request, banner_form):
    print(request.POST)
    product_created = True
    position = banner_form.cleaned_data['position']
    status = banner_form.cleaned_data['status']

    media_content = banner_form.cleaned_data['media_content']
    media_link = banner_form.cleaned_data['media_link']

    banner_form = None
    if not banner_form:
        print(request)
        print(request.POST)

        banner_form = Banners(position=position, status=status,
                              media_content=media_content, media_link=media_link,
                              )

        banner_form.save()

        print(request.POST)
        # use django messages framework
    messages.success(request,
                     "Yeeew, check it out on the home page!")

   # return HttpResponseRedirect("/admin/design/")
    return HttpResponseRedirect(reverse_lazy('core:BannerView'))

# return HttpResponse("OK")
# return redirect(reverse('vendors:ProductsList'))


class BannerCdreate(View):
    def get(self, request, *args, **kwargs):
        print(request)

        return render(request, "design/banner/add-banner.html",
                      )

    print(request)

    def post(self, request, *args, **kwargs):
        position = request.POST.get("position")
        status = request.POST.get("status")
        sort_order = request.POST.get("sort_order")
        media_content = request.FILES.get("media_content")
        media_link = request.POST.get("media_link")
        media_location = request.POST.get("media_location")
        print(request.POST)
        # status = request.POST.get("status")
        banner = Banners(position=position, status=status, sort_order=sort_order, media_content=media_content,
                         media_link=media_link, media_location=media_location
                         )
        banner.save()
        # return HttpResponse("OK")
        return HttpResponseRedirect(reverse_lazy('core:BannerView'))


############ Menu ##############

class MenuView(TemplateView):
    template_name = "design/slider/sliders-admin.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sliders'] = Slider.objects.all()
        return context


class MenuDetailView(DetailView):
    model = Slider
    context_object_name = 'slider'
    template_name = 'design/slider/slider-detail.html'


class MenuGroupCreate(CreateView):
    model = SliderGroup
    fields = '__all__'
    template_name = 'design/slider/add-slider-group.html'
    success_url = reverse_lazy('core:SliderView')


class MenuDelete(DeleteView):
    model = Slider
    fields = '__all__'
    template_name = 'design/slider/confirm_delete.html'
    success_url = reverse_lazy('core:SliderView')
