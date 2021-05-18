from django.core.exceptions import NON_FIELD_ERRORS
from django.db import models
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status


class EasyAPI(models.Model, APIView):
    """
    Inherite EasyAPI class and create models as you were creating.
    You need to add a url with the child class.
    For example:

    in models.py

    class MyClass(EasyAPI):
        field1 = models.CharField(max_length=100)

    in urls.py
    from easy_api.models import EasyAPI
    from .models import MyClass

    urlpaterns = [
        path('myurl/', EasyAPI.as_view(), {'child_class': MyClass})
    ]
    """
    def get(self, request, *args, **kwargs):
        

        class EasyAPISerializer(serializers.ModelSerializer):
            class Meta:
                fields = '__all__'
                model = kwargs['child_model']

        self.child_model = kwargs['child_model']
        
        pk = None
        if 'id' in request.query_params:
            pk = request.query_params['id']

        try:
            queryset = self.child_model.objects.all() if pk is None else self.child_model.objects.get(pk=pk)
        except self.child_model.DoesNotExist:
            return Response({'msg': f'object with id={pk} does not exists'}, status=status.HTTP_404_NOT_FOUND)
        if pk is None:
            easyapi_serializer = EasyAPISerializer(queryset, many=True)
        else:
            easyapi_serializer = EasyAPISerializer(queryset)

        return Response(easyapi_serializer.data)
    
    def post(self, request, *args, **kwargs):
        
        class EasyAPISerializer(serializers.ModelSerializer):
            class Meta:
                fields = '__all__'
                model = kwargs['child_model']

        easyapi_serializer = EasyAPISerializer(data=request.data)
        easyapi_serializer.is_valid(raise_exception=True)
        easyapi_serializer.save()

        return Response(easyapi_serializer.data)
    
    def put(self, request, *args, **kwargs):
        
        pk = None
        if 'id' not in request.query_params:
            return Response({'msg': 'id parameter not present.'}, status=status.HTTP_400_BAD_REQUEST)

        pk = request.query_params['id']

        class EasyAPISerializer(serializers.ModelSerializer):
            class Meta:
                fields = '__all__'
                model = kwargs['child_model']
        try:
            queryset = kwargs['child_model'].objects.get(pk=pk)
            easy_serializer = EasyAPISerializer(queryset, data=request.data, partial=True)
            easy_serializer.is_valid(raise_exception=True)
            easy_serializer.save()

            return Response(easy_serializer.data)
        except kwargs['child_model'].DoesNotExist:
            return Response({'msg': f'object with id={pk} does not exists'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        
        pk = None
        if 'id' not in request.query_params:
            return Response({'msg': 'id parameter not present.'}, status=status.HTTP_400_BAD_REQUEST)
        
        pk = request.query_params['id']

        queryset = kwargs['child_model'].objects.filter(pk=pk)

        if len(queryset)==0:
            return Response({'msg': f'object with id={pk} does not exists'}, status=status.HTTP_404_NOT_FOUND)

        queryset.delete()
        return Response({'msg': 'Object deleted'})

