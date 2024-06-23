from rest_framework import serializers
from .models import Commento

class CommentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commento
        fields = ['contenuto']

class createCommentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commento
        fields = ['risorsa','contenuto']