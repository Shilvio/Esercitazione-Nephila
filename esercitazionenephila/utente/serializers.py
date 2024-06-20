from rest_framework import serializers
from .models import Utente

class UtenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utente
        fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utente
        fields = ['username','password','ruolo']

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utente
        fields = ['username','password']