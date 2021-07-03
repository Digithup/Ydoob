from datetime import datetime

from django.core.files.storage import FileSystemStorage
from django.db import transaction
from django.forms import formset_factory
from django.http import request, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, DetailView, DeleteView, CreateView
from core.models.design import Slider, SliderGroup, SliderMedia, Banners


class SliderView(TemplateView):
    template_name = "Slider/sliders-admin.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sliders'] = Slider.objects.all()
        return context


class SliderDetailView(DetailView):
    model = Slider
    context_object_name = 'slider'
    template_name = 'slider/slider-detail.html'


class SliderGroupCreate(CreateView):
    model = SliderGroup
    fields = '__all__'
    template_name = 'slider/add-slider-group.html'
    success_url = reverse_lazy('core:SliderView')


class SliderDelete(DeleteView):
    model = Slider
    fields = '__all__'
    template_name = 'slider/confirm_delete.html'
    success_url = reverse_lazy('core:SliderView')


class SliderCreate(View):
    def get(self, request, *args, **kwargs):
        print(request)
        groups = SliderGroup.objects.filter(status=True)

        return render(request, "slider/slider-create.html",
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
        return render(request, 'slider/sliders-admin.html')


class BannersView(TemplateView):
    template_name = "banner/banners-admin.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['banners'] = Banners.objects.all()
        return context


class BannerDetailView(DetailView):
    model = Banners
    context_object_name = 'banner'
    template_name = 'banner/banner-detail.html'


class BajnnerCreate(CreateView):
    model = Banners
    fields = '__all__'
    template_name = 'banner/add-banner.html'
    success_url = reverse_lazy('core:BannerView')


class BannerDelete(DeleteView):
    model = Banners
    fields = '__all__'
    template_name = 'banner/confirm_delete.html'
    success_url = reverse_lazy('core:BannerView')


class BannerCreate(View):
    def get(self, request, *args, **kwargs):
        print(request)

        return render(request, "banner/add-banner.html",
                     )

    print(request)

    def post(self, request, *args, **kwargs):
        title = request.POST.get("title")
        status = request.POST.get("status")
        sort_order = request.POST.get("sort_order")
        media_content = request.FILES.get("media_content")
        media_link = request.POST.get("media_link")
        media_location = request.POST.get("media_location")
        print(request.POST)
        # status = request.POST.get("status")
        banner = Banners(title=title, status=status, sort_order=sort_order,media_content=media_content,
                         media_link=media_link,media_location=media_location
                     )
        banner.save()
        # return HttpResponse("OK")
        return render(request, 'banner/banners-admin.html')


############ Menu ##############

class MenuView(TemplateView):
    template_name = "Slider/sliders-admin.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sliders'] = Slider.objects.all()
        return context


class MenuDetailView(DetailView):
    model = Slider
    context_object_name = 'slider'
    template_name = 'slider/slider-detail.html'


class MenuGroupCreate(CreateView):
    model = SliderGroup
    fields = '__all__'
    template_name = 'slider/add-slider-group.html'
    success_url = reverse_lazy('core:SliderView')


class MenuDelete(DeleteView):
    model = Slider
    fields = '__all__'
    template_name = 'slider/confirm_delete.html'
    success_url = reverse_lazy('core:SliderView')


