# Create your views here.
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import *
from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from risorsa import views as viewsRisorsa
from risorsa import serializers as risorsaSerializer

def searchNodiChild(nodo):
    try:
        nodiChild = Nodo.objects.filter(padre= nodo).all()
        return nodiChild
    except Nodo.DoesNotExist:
        return None


# crea il nodo child
def postNodoChild(request,nodo_id):
    nodo = searchNodo(nodo_id)
    if not nodo:
        return Response({"details": "Nessun nodo padre presente sul quale caricare la risorsa"},status=status.HTTP_404_NOT_FOUND)
    if nodo.owner.id == request.user.id:
        return postNodo(request,nodo.id)
    else:
        return Response({"details":"Non autorizzato"}, status=status.HTTP_401_UNAUTHORIZED)

def searchNodoPadre(nodo_id):
    try :
        nodo = Nodo.objects.get(id=nodo_id)
        padre = nodo.padre
        return padre
    except Nodo.DoesNotExist:
        return None


def searchNodo(nodo_id):
    try :
        nodo = Nodo.objects.get(id=nodo_id)
        return nodo
    except Nodo.DoesNotExist:
        return None

def getNodo(nodo_id):
    nodo = searchNodo(nodo_id)
    if not nodo:
        return Response({"details": "Nessun nodo presente"},status=status.HTTP_404_NOT_FOUND)
    serializer = NodoSerializer(nodo, many=False)
    figli = searchNodiChild(nodo)
    risorse = viewsRisorsa.searchRisorsaNodo(nodo_id)
    figliData = NodoSerializer(figli, many=True).data if figli else None
    risorseData = risorsaSerializer.RisorsaNodoSerializer(risorse ,many=True).data if risorse else None
    return Response({"nodo": serializer.data, "figli":figliData, "risorse":risorseData} )

def deleteNodo(request,nodo_id):
    nodo = searchNodo(nodo_id)
    if nodo.owner.id == request.user.id:
        if not nodo:
            return Response({"details": "Nessun nodo presente"},status=status.HTTP_404_NOT_FOUND)
        serializer = NodoSerializer(nodo, many=False)
        figli = searchNodiChild(nodo)
        risorse = viewsRisorsa.searchRisorsa(nodo)
        if ((not figli) and (not risorse)):
            nodo.delete()
            return Response({"details": "nodo "+ str(serializer.data['id']) + " cancellato"})

    else:
        return Response({"details":"Non autorizzato"}, status=status.HTTP_401_UNAUTHORIZED)

def putTitoloNodo(request,nodo_id):
    nodo = searchNodo(nodo_id)
    if ((not request.data)or(request.data['titolo'] in [None,''])):
        return Response({"details": "Richeista malformata"}, status=status.HTTP_400_BAD_REQUEST)
    if nodo.owner.id == request.user.id:
        if not nodo:
            return Response({"details": "Nessun nodo presente"},status=status.HTTP_404_NOT_FOUND)
        nodo.titolo = request.data['titolo']
        serializer = ModificaNodoSerializer(nodo,data=request.data ,many=False)
        if serializer.is_valid():
            serializer.save()
            return Response({"nodo": serializer.data},status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"details":"Non autorizzato"}, status=status.HTTP_401_UNAUTHORIZED)


# crea il nodo root
def postNodo(request,padre):

    if ((not request.data)or(request.data['titolo'] in [None,''])):
        return Response({"details": "Richeista malformata"}, status=status.HTTP_400_BAD_REQUEST)
    serializer = CreateNodoSerializer(data={'owner':request.user.id,'padre':padre,'titolo':request.data['titolo']})
    if serializer.is_valid():
        serializer.save()
        return Response({"nodo": serializer.data})
    return Response({"details": "Richeista malformata"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def postNodoRoot(request):
    return postNodo(request,None)


@api_view(['POST'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def postNuovoChildInPadre(request,nodo_id):
    padre = searchNodoPadre(nodo_id)
    if not padre:
        return Response({"details": "Nessun nodo padre presente sul quale caricare la risorsa"},status=status.HTTP_404_NOT_FOUND)
    if padre.owner.id == request.user.id:
        return postNodo(request,padre.id)
    else:
        return Response({"details":"Non autorizzato"}, status=status.HTTP_401_UNAUTHORIZED)



# Create your views here.
@api_view(['GET','POST','DELETE','PUT'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def nodoHandler(request,nodo_id):
    if request.method == 'GET':
        return getNodo(nodo_id)
    elif request.method == 'POST':
        return postNodoChild(request,nodo_id)
    elif request.method == 'DELETE':
        return deleteNodo(request,nodo_id)
    elif request.method == 'PUT':
        return putTitoloNodo(request,nodo_id)

