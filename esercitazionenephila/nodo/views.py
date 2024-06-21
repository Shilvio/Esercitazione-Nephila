# Create your views here.
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Utente
from .serializers import *
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated

#crea nodi
def getNodi(request):
    nodi = Nodo.objects.all()
    if not nodi:
        return Response({"detail": "Nessun nodo presente"},status=status.HTTP_404_NOT_FOUND)
    serializer = NodoSerializer(nodi, many=True)
    return Response({"nodi": serializer.data})

# crea il nodo root
def postNodo(request):

    serializer = CreateNoidoSerializer(data={'owner':request.user.id,'padre':None})
    if serializer.is_valid():
        serializer.save()
        return Response({"nodo": serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Create your views here.
@api_view(['GET','POST'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def nodiViews(request):
    if request.method == 'GET':
        return getNodi(request)
    elif request.method == 'POST':
        return postNodo(request)



# crea il nodo child
@api_view(['POST'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def postNodoChild(request):

    serializer = CreateNoidoSerializer(data={'owner':request.user.id,'padre':None})
    if serializer.is_valid():
        serializer.save()
        return Response({"nodo": serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

