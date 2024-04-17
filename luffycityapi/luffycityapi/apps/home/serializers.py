from rest_framework import serializers
from .models import Nav

class NavModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = Nav
        fields = ['name','link','is_http']