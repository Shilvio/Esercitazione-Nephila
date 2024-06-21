from rest_framework import serializers
from .models import Nodo

class NodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nodo
        fields = ['id','owner','padre']

class CreateNoidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nodo
        fields = ['owner','padre']