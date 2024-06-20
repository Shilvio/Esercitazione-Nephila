from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework import status

from .models import Utente

from .serializers import *

# Create your views here.
@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        utente = Utente.objects.get(username = request.data["username"])
        token = Token.onject.create(utente = utente)
        return Response({"token": token.key, "utente" : utente.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data = request.data)
    try:
        utente = Utente.objects.get(username = request.data["username"])
    except Utente.DoesNotExist:
            return Response({"detail": "Utente not found"},status=status.HTTP_404_NOT_FOUND)
    if request.data["password"] == utente.password:
        token = Token.objects.create(user = utente)
        return Response({"token": token.key, "utente" : utente.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def getUser(request):
    return Response()
