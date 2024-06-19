from rest_framework import serializers
from utente.models import Utente
from risorsa.models import Risorsa

class UtenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utente
        fields = '__all__'

class RisorsaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Risorsa
        fields = '__all__'