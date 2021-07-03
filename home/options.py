import datetime
import json

from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.defaultfilters import title
# Create your views here.
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import UpdateView, CreateView, ListView, DeleteView, DetailView

from catalog.forms import ProductAddForm, ManufacturerAddForm, ProductFullForm
from catalog.models import Category, Product, Tag, Image
from home.forms import SearchForm


def options(request):
    categories = Category.objects.all()

    context = {
        'categories': categories
    }
    # return HttpResponse(1)
    return render(request, 'admin/pages/../core/templates/catalog/admin_manufacture.html', context)


class AddOptions(CreateView):
    model = Category
    template_name = 'admin/pages/../core/templates/add-manufacture.html'
    fields = '__all__'
    # uccess_url =redirect('home:product_admin')
    success_url = reverse_lazy('home:category')


class EditOptions(UpdateView):
    model = Category
    fields = '__all__'
    template_name = 'admin/pages/../core/templates/catalog/edit-manufacture.html'
    success_url = reverse_lazy('home:category')


class DeleteOptions(DeleteView):
    model = Category
    fields = '__all__'
    template_name = 'admin/pages/message/category_confirm_delete.html'
    success_url = reverse_lazy('home:category_admin')
