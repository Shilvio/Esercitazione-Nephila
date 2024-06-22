from rest_framework import serializers
from .models import Risorsa

class RisorsaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Risorsa
        fields = ['id','owner','nodo','titolo','contenuto','responsabile','operatore','id']

class CreateRisorsaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Risorsa
        fields = ['owner','nodo','titolo','contenuto','responsabile','operatore']