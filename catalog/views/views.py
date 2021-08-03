from dal import autocomplete
from django.http import HttpResponse, request, JsonResponse
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
from catalog.models.product_options import Filters


def index(request):
    catdata = Categories.objects.all()
    products = Products.objects.all
    page = "home"
    context = {
        'page': page,
        'catdata': catdata,
        'products': Products,
    }
    return render(request, 'admin/index.html', context)


class CatList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'admin/pages/admin_manufacture.html'

    def get(self, request):
        queryset = Categories.objects.all()
        return Response({'categories': queryset})


def FilterSearch(request):
    title = request.GET.get('filter')
    payload = []
    if filter:
        filters_obj = Filters.objects.filter(title=title)
        for filter_obj in filters_obj:
            payload.append(filter_obj.title)
        else:
            filters_obj = Filters.objects.all()
            for filter_obj in filters_obj:
                payload.append(filter_obj.title)
    return JsonResponse({'status': 200, 'data': payload})


def FilterSearchb(request):

    # request should be ajax and method should be GET.

    if request.is_ajax and request.method == "GET":

        # get the nick name from the client side.

        nick_name = request.GET.get("nick_name", None)

        # check for the nick name in the database.

        if Filters.objects.filter(title = nick_name).exists():

            # if nick_name found return not valid new friend

            return JsonResponse({"valid":False}, status = 200)

        else:

            # if nick_name not found, then user can create a new friend.

            return JsonResponse({"valid":True}, status = 200)


    return JsonResponse({}, status = 400)

def FilterSearcssh(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': Filters.objects.filter(title=username)
    }
    if data['is_taken']:
        data['error_message'] = 'A user with this username already exists.'
    return JsonResponse(data)
