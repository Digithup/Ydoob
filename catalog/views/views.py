from django.http import HttpResponse, request
from django.shortcuts import render, redirect, get_object_or_404
# Create your views here.
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.
from haystack.query import SearchQuerySet
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from catalog.models.models import Categories, Products



def index(request):

    catdata = Categories.objects.all()
    products = Products.objects.all
    page = "home"
    context = {
        'page': page,
        'catdata':catdata,
        'products':Products,
    }
    return render(request, 'admin/index.html', context)


def sidebar(request):

    catdata = Categories.objects.all()
    page = "home"
    context = {
        'page': page,
        'catdata':catdata
    }
    return render(request, 'admin/sidebar.html', context)


def category_list(request):
    catdata = Categories.objects.all()
    context = {
               # 'category':category,
               'catdata': catdata}
    #return HttpResponse(1)
    return render(request, 'front/pages/../../home/templates/categories.html', context)


def Products_list(request, category_slug=None):
    category = None
    catdata = Categories.objects.all()
    products = Products.objects.filter(status=True)
    if category_slug:
        category = get_object_or_404(Categories, slug=category_slug)
        products = Products.objects.filter(category=category)

    context = {'Products': Products,
                'category':category,
               'catdata': catdata}
    #return HttpResponse(1)
    return render(request, 'catalog/category/admin-category.html', context)


def user_list(request, id, slug):
    # query = request.GET.get('q')

    # usersaaa = UserProfile.objects.all()

    return HttpResponse('h')
# return render(request,'admin/stores-list.html')








class CatList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'admin/pages/admin_manufacture.html'

    def get(self, request):
        queryset = Categories.objects.all()
        return Response({'categories': queryset})



