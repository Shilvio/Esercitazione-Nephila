from rest_framework import serializers
from .models import Utente

class UtenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utente
        fields = ['id','ruolo','username']

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utente
        fields = ['username','password','ruolo']