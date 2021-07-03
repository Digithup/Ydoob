##### get data from model ---------> json
from rest_framework import routers, serializers, viewsets
from catalog.models.models import Category, Product, Image
from core.models.design import Slider


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slider
        fields = ('caption',)