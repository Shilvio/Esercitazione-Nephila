from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from utente.models import Utente
from risorsa.models import Risorsa
from .serializers import *

@api_view(['GET'])
def GetUtente(req):
    utente = Utente.objects.all()
    serializer = UtenteSerializer(utente, many = True)
    return Response(serializer.data)

@api_view(['GET'])
def GetRrisorsa(req):
    risorsa = Risorsa.objects.all()
    serializer = RisorsaSerializer(risorsa, many = True)
    return Response(serializer.data)

