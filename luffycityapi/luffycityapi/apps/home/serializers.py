from rest_framework import serializers
from .models import Nav,Banner

class NavModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = Nav
        fields = ['name','link','is_http']

class BannerModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['image','name','link','is_http']