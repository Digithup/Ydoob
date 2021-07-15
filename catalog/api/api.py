##### get data from model ---------> json
from rest_framework import generics
from rest_framework.renderers import JSONRenderer

from catalog.models.models import Categories, Products
from catalog.api.serializers import CategorySerializer, Productserializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes


@api_view(['GET'])
@renderer_classes([JSONRenderer])
def category_list_api(request):
    all_category = Categories.objects.all()
    data = CategorySerializer(all_category , many=True).data
    return Response({'data':data})

@api_view(['GET'])
def category_details_api(request,id):
    category_detail = Categories.objects.get(id=id)
    data = CategorySerializer(category_detail ).data
    return Response({'data':data})

#####Clas based


class CategoryListAPi(generics.ListCreateAPIView):
    model = Categories
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer



class CategoryApi(generics.RetrieveUpdateDestroyAPIView):
    model = Categories
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'id'


class ProductsListApi(generics.ListCreateAPIView):
    model = Products
    #queryset = Products.objects.all()
    serializer_class = Productserializer



class ProductsApi(generics.RetrieveUpdateDestroyAPIView):
    model = Products
    #queryset = Products.objects.all()
    serializer_class = Productserializer
    lookup_field = 'id'

