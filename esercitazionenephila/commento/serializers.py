from rest_framework import serializers
from .models import Commento

class CommentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commento
        fields = ['contenuto']

class CreateCommentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commento
        fields = ['risorsa','contenuto']