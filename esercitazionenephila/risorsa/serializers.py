from rest_framework import serializers
from .models import Risorsa

class RisorsaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Risorsa
        fields = ['titolo','contenuto']

class CreateRisorsaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Risorsa
        fields = ['owner','nodo','titolo','contenuto','responsabile','operatore']

class RisorsaNodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Risorsa
        fields = ['titolo']

class ModificaRisorsaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Risorsa
        fields = ['titolo','contenuto']