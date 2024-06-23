from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Risorsa
from .serializers import *
from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from commento import views as commentoViews
from commento import serializers as serializersCommento
from nodo import views as nodoViews

def validateRole(utente,risorsa):
    if risorsa.owner.id == utente.id:
         return True
    elif utente.ruolo == 0  and risorsa.operatore:
        return True
    elif utente.ruolo == 1  and risorsa.responsabile:
        return True
    else:
        return False

def searchRisorsaNodo(nodo_id):
    try :
        risorse = Risorsa.objects.filter(nodo=nodo_id).all()
        return risorse
    except Risorsa.DoesNotExist:
        return None


def searchRisorsa(risorsa_id):
    try :
        risorsa = Risorsa.objects.get(id=risorsa_id)
        return risorsa
    except Risorsa.DoesNotExist:
        return None


def getRisorsa(request,risorsa_id):
    risorsa = searchRisorsa(risorsa_id)
    if not risorsa:
            return Response({"details": "Nessun risorsa presente"},status=status.HTTP_404_NOT_FOUND)
    if validateRole(request.user,risorsa):
        serializer = RisorsaSerializer(risorsa, many=False)
        commenti = commentoViews.searchCommenti(risorsa_id)
        commentiData = serializersCommento.CommentoSerializer(commenti, many=True).data if commenti else None

        return Response({"risorsa": serializer.data, "commenti":commentiData } )
    else:
        return Response({"details":"Non autorizzato"}, status=status.HTTP_401_UNAUTHORIZED)


def deleteRisorsa(request,risorsa_id):
    risorsa = searchRisorsa(risorsa_id)
    if risorsa.owner.id == request.user.id:
        if not risorsa:
            return Response({"details": "Nessun risorsa presente"},status=status.HTTP_404_NOT_FOUND)
        serializer = RisorsaSerializer(risorsa, many=False)
        risorsa.delete()
        return Response({"details": "risorsa "+ str(serializer.data['id']) + " cancellato"})

    else:
        return Response({"details":"Non autorizzato"}, status=status.HTTP_401_UNAUTHORIZED)

def putRisorsa(request,risorsa_id):
    risorsa = searchRisorsa(risorsa_id)
    if not risorsa:
        return Response({"details": "Nessun risorsa presente"},status=status.HTTP_404_NOT_FOUND)
    if not request.data:
            return Response({"details": "Richeista malformata"}, status=status.HTTP_400_BAD_REQUEST)
    if request.data['titolo'] not in [None,'']:
        risorsa.titolo = request.data['titolo']
    if request.data['contenuto'] not in [None,'']:
        risorsa.contenuto = request.data['contenuto']
    serializer = ModificaRisorsaSerializer(risorsa, data=request.data, many=False)
    if serializer.is_valid():
        serializer.save()
        return Response({"risorsa": serializer.data})
    print(serializer.errors)
    return Response({"details": "Richeista malformata"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def postRisorsa(request,nodo_id):
    nodo = nodoViews.searchNodo(nodo_id)
    if not nodo:
        return Response({"details": "Nessun nodo presente sul quale caricare la risorsa"},status=status.HTTP_404_NOT_FOUND)
    if nodo.owner.id == request.user.id:

        if ((not request.data)or(request.data['titolo'] in [None,''])or(request.data['contenuto'] in [None,''])):
            return Response({"details": "Richeista malformata"}, status=status.HTTP_400_BAD_REQUEST)
        request.data['owner']=request.user.id
        request.data['nodo']= nodo_id
        serializer = CreateRisorsaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"risorsa": serializer.data})
        print(serializer.errors)
        return Response({"details": "Richeista malformata"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"details":"Non autorizzato"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET','DELETE','PUT'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def risorsaIdHandler(request,nodo_id,risorsa_id):
    if request.method == 'GET':
        return getRisorsa(request,risorsa_id)
    elif request.method == 'DELETE':
        return deleteRisorsa(request,risorsa_id)
    elif request.method == 'PUT':
        return putRisorsa(request,risorsa_id)

@api_view(['POST'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def postNuovaRisorsaPadre(request,nodo_id):
    padre = nodoViews.searchNodoPadre(nodo_id)
    if not padre:
        return Response({"details": "Nessun nodo padre presente sul quale caricare la risorsa"},status=status.HTTP_404_NOT_FOUND)
    if padre.owner.id == request.user.id:
        if ((not request.data)or(request.data['titolo'] in [None,''])or(request.data['contenuto'] in [None,''])):
            return Response({"details": "Richeista malformata"}, status=status.HTTP_400_BAD_REQUEST)
        request.data['owner']=request.user.id
        request.data['nodo']= padre.id
        serializer = CreateRisorsaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"risorsa": serializer.data})
        print(serializer.errors)
        return Response({"details": "Richeista malformata"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"details":"Non autorizzato"}, status=status.HTTP_401_UNAUTHORIZED)
