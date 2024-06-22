from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Risorsa
from .serializers import *
from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from nodo import views as nodoViews


def searchRisorsa(risorsa_id):
    try :
        risorsa = Risorsa.objects.get(id=risorsa_id)
        return risorsa
    except Risorsa.DoesNotExist:
        return None


def getRisorsa(risorsa_id):
    risorsa = searchRisorsa(risorsa_id)
    if not risorsa:
        return Response({"details": "Nessun risorsa presente"},status=status.HTTP_404_NOT_FOUND)
    serializer = RisorsaSerializer(risorsa, many=False)
    return Response({"risorsa": serializer.data} )

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


@api_view(['POST'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def postRisorsa(request,nodo_id):
    nodo = nodoViews.searchNodo(nodo_id)
    print(request.data['operatore'] in [None])
    print("ciao")
    if not nodo:
        return Response({"details": "Nessun nodo presente sul quale caricare la risorsa"},status=status.HTTP_404_NOT_FOUND)
    if nodo.owner.id == request.user.id:

        if ((not request.data)or(request.data['titolo'] in [None,''])or(request.data['contenuto'] in [None,''] or (request.data['operatore'] in [None,''])or (request.data['responsabile'] in [None,'']))):

            return Response({"details": "Richeista malformata"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = CreateRisorsaSerializer(data={'owner':request.user.id,
                                                   'nodo':nodo_id,
                                                   'titolo':request.data['titolo'],
                                                   'contenuto':request.data['contenuto'],
                                                   'responsabile':request.data['responsabile'],
                                                   'operatore':request.data['operatore']})
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
def risorsaViews(request,nodo_id,risorsa_id):
    if request.method == 'GET':
        return getRisorsa(risorsa_id)
    elif request.method == 'DELETE':
        return deleteRisorsa(request,risorsa_id)
    elif request.method == 'PUT':
        return putRisorsa(request,risorsa_id)

