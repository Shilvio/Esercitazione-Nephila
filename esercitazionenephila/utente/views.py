from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Utente

from .serializers import *

# Create your views here.
@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        utente = Utente.objects.get(username = request.data["username"])
        token = Token.objects.create(user = utente)
        return Response({"token": token.key, "utente" : {utente.username, utente.ruolo}},status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data = request.data)
    try:
        utente = Utente.objects.get(username = request.data["username"])
    except Utente.DoesNotExist:
            return Response({"detail": "Utente not found"},status=status.HTTP_404_NOT_FOUND)
    if request.data["password"] == utente.password:
        try:
            token = Token.objects.get(user_id=utente.id)
        except Token.DoesNotExist:
            token = Token.objects.create(user = utente)
        return Response({"token": token.key, "utente" : {utente.username, utente.ruolo}})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def testToken(request):
    return Response("auth verified passed for {}".format(request.user.ruolo))

