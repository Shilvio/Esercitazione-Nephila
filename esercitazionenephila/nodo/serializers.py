from rest_framework import serializers
from .models import Nodo

class NodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nodo
        fields = ['titolo']

class CreateNodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nodo
        fields = ['owner','padre','titolo']