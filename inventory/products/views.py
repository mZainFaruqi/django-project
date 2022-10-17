from django.http import HttpResponse
from django.shortcuts import render
from kombu.asynchronous.http import Response
from django.contrib.auth import get_user_model;
from django_celery_beat.models import PeriodicTask, CrontabSchedule

# Create your views here.

from rest_framework import generics


from .models import Product
from .serializers import ProductSerializer
from core.mixins import  StaffEditorPermissionMixin
from .tasks import test_func

class ProductListCreateApiView(StaffEditorPermissionMixin, generics.ListCreateAPIView):
    #test_func.delay()
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # lookup_field= 'pk'

    # def list(self,request):
    #     queryset = self.get_queryset()
    #     serializer = ProductSerializer(queryset,many=True)
    #     test_func.delay()
    #     return Response(serializer.data)
    print(get_user_model().objects.all())
    def perform_create(self, serializer):
        print(serializer.validated_data)
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None
        if content is None:
            content = title
        serializer.save(content=content)


product_list_create_view = ProductListCreateApiView.as_view()

class ProductDetailApiView(StaffEditorPermissionMixin,generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # lookup_field= 'pk'


product_detail_view = ProductDetailApiView.as_view()


class ProductUpdateApiView(StaffEditorPermissionMixin,generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def perform_update(self, serializer):
        instance = serializer.save();
        if not instance.content:
            instance.content = instance.title


product_update_view = ProductUpdateApiView.as_view()


class ProductDestroyApiView(StaffEditorPermissionMixin,generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        super().perform_destroy(instance)


product_destroy_view = ProductDestroyApiView.as_view()

def test(request):
    test_func.delay()
    return HttpResponse("Done")