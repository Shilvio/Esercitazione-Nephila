from rest_framework import serializers
from .models import Risorsa

class RisorsaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Risorsa
        fields = '__all__'
