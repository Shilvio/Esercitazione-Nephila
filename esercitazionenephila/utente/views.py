from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework import status
from .models import Utente
from .serializers import *
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# api handler per registrare un utente
@swagger_auto_schema(
    tags=['utenti'],
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, default='user'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, default='user'),
            'ruolo' : openapi.Schema(type=openapi.TYPE_NUMBER,enum=[0,1,2]),
        },
        required=['username', 'password']
    ),
    responses={
        201: 'Created',
        400: 'Bad Request',
        404: 'Not Found'
    }
)
@api_view(['POST'])
def register(request):
    try:
        serializer = RegisterSerializer(data = request.data)
    except:
        return Response({"details": "Richeista malformata"}, status=status.HTTP_400_BAD_REQUEST)
    if request.data:
        if request.data["ruolo"] == 2:
            return Response("ruolo 2 non permesso", status=status.HTTP_400_BAD_REQUEST)
    else:
            return Response("Richiesta malformata", status=status.HTTP_400_BAD_REQUEST)
    if serializer.is_valid():
        serializer.save()
        utente = Utente.objects.get(username = request.data["username"])
        token = Token.objects.create(user = utente)
        return Response({"token": token.key, "utente" : {utente.username, utente.ruolo}},status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# api handler per loggare un utente
@swagger_auto_schema(
    tags=['utenti'],
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, default='user'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, default='user'),
        },
        required=['username', 'password']
    ),
    responses={
        201: 'Created',
        400: 'Bad Request',
        404: 'Not Found'
    }
)
@api_view(['POST'])
def login(request):

    try:
        utente = Utente.objects.get(username = request.data["username"], password=request.data["password"])
    except Utente.DoesNotExist:
            return Response({"detail": "Utente not found"},status=status.HTTP_404_NOT_FOUND)
    except:
        return Response({"details": "Richeista malformata"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        token = Token.objects.get(user_id=utente.id).delete()
        token = Token.objects.create(user = utente)
    except Token.DoesNotExist:
        token = Token.objects.create(user = utente)
    serializer = UtenteSerializer(utente)
    return Response({"token": token.key, "utente" : serializer.data},status=status.HTTP_201_CREATED)

