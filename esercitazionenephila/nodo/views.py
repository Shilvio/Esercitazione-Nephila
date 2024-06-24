# Create your views here.
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import *
from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from risorsa import views as views_risorsa
from risorsa import serializers as risorsa_serializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# cerca nodi child nel padre
def search_nodi_child(nodo):
    try:
        nodiChild = Nodo.objects.filter(padre= nodo).all()
        return nodiChild
    except Nodo.DoesNotExist:
        return None


# crea il nodo child
def post_nodo_child(request,nodo_id):
    nodo = search_nodo(nodo_id)
    if not nodo:
        return Response({"details": "Nessun nodo padre presente sul quale caricare la risorsa"},status=status.HTTP_404_NOT_FOUND)
    if nodo.owner.id == request.user.id:
        return post_nodo(request,nodo.id)
    else:
        return Response({"details":"Non autorizzato"}, status=status.HTTP_401_UNAUTHORIZED)

# cerca il padrte da un nodo child
def search_nodo_padre(nodo_id):
    try :
        nodo = Nodo.objects.get(id=nodo_id)
        padre = nodo.padre
        return padre
    except Nodo.DoesNotExist:
        return None

# cerca un nodo dall'id
def search_nodo(nodo_id):
    try :
        nodo = Nodo.objects.get(id=nodo_id)
        return nodo
    except Nodo.DoesNotExist:
        return None

# ritorna un nodo, i child se presentri e le risorse se presenti
def get_nodo(nodo_id):
    nodo = search_nodo(nodo_id)
    if not nodo:
        return Response({"details": "Nessun nodo presente"},status=status.HTTP_404_NOT_FOUND)
    serializer = NodoSerializer(nodo, many=False)
    figli = search_nodi_child(nodo)
    risorse = views_risorsa.search_risorsa_nodo(nodo_id)
    figli_data = NodoSerializer(figli, many=True).data if figli else None
    risorse_data = risorsa_serializer.RisorsaNodoSerializer(risorse ,many=True).data if risorse else None
    return Response({"nodo": serializer.data, "figli":figli_data, "risorse":risorse_data} )

# elimina il nodo
def delete_nodo(request,nodo_id):
    nodo = search_nodo(nodo_id)
    if not nodo:
            return Response({"details": "Nessun nodo presente"},status=status.HTTP_404_NOT_FOUND)
    try:
        if nodo.owner.id == request.user.id:
            serializer = NodoSerializer(nodo, many=False)
            figli = search_nodi_child(nodo)
            risorse = views_risorsa.search_risorsa(nodo)
            if ((not figli) and (not risorse)):
                nodo.delete()
                return Response({"details": "nodo "+ str(serializer.data['id']) + " cancellato"})

    except:
        return Response({"details":"Non autorizzato"}, status=status.HTTP_401_UNAUTHORIZED)

# modifica il titolo del nodo
def put_titolo_nodo(request,nodo_id):
    nodo = search_nodo(nodo_id)
    try:
        if ((not request.data)or(request.data['titolo'] in [None,''])):
            return Response({"details": "Richeista malformata"}, status=status.HTTP_400_BAD_REQUEST)
    except:
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
def post_nodo(request,padre):

    try:
        if ((not request.data)or(request.data['titolo'] in [None,''])):
            return Response({"details": "Richeista malformata"}, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({"details": "Richeista malformata"}, status=status.HTTP_400_BAD_REQUEST)
    serializer = CreateNodoSerializer(data={'owner':request.user.id,'padre':padre,'titolo':request.data['titolo']})
    if serializer.is_valid():
        serializer.save()
        return Response({"nodo": serializer.data},status=status.HTTP_201_CREATED)
    return Response({"details": "Richeista malformata"}, status=status.HTTP_400_BAD_REQUEST)

# api view handler per nodo root
@swagger_auto_schema(
    tags=['nodi'],
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'titolo': openapi.Schema(type=openapi.TYPE_STRING, default='titolo test'),
        },
        required=['titolo']
    ),
    responses={
        201: 'Created',
        400: 'Bad Request',
    }
)
@api_view(['POST'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def post_nodo_root(request):
    return post_nodo(request,None)

# api view handler per postare nodo in padre
@swagger_auto_schema(
    tags=['nodi'],
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'titolo': openapi.Schema(type=openapi.TYPE_STRING, default='titolo test'),
        },
        required=['titolo']
    ),
    responses={
        201: 'Created',
        400: 'Bad Request',
        404: 'Not Found'
    }
)
@api_view(['POST'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def post_nuovo_child_in_padre(request,nodo_id):
    padre = search_nodo_padre(nodo_id)
    if not padre:
        return Response({"details": "Nessun nodo padre presente sul quale caricare la risorsa"},status=status.HTTP_404_NOT_FOUND)
    if padre.owner.id == request.user.id:
        return post_nodo(request,padre.id)
    else:
        return Response({"details":"Non autorizzato"}, status=status.HTTP_401_UNAUTHORIZED)

# api view handler per operazioni put delete e get nodi child e nodi normali
@swagger_auto_schema(
    tags=['nodi'],
    methods=['post'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'titolo': openapi.Schema(type=openapi.TYPE_STRING, default='titolo test'),
        },
        required=['titolo']
    ),
    responses={
        201: 'Created',
        400: 'Bad Request',
        404: 'Not Found'
    }
)
@swagger_auto_schema(
    tags=['nodi'],
    methods=['put'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'titolo': openapi.Schema(type=openapi.TYPE_STRING, default='titolo test'),
        },
        required=['titolo']
    ),
    responses={
        200: 'Ok',
        400: 'Bad Request',
        404: 'Not Found'
    }
)
@swagger_auto_schema(
    tags=['nodi'],
    methods=['get','delete'],
    responses={
        201: 'Created',
        400: 'Bad Request',
        404: 'Not Found'
    }
)
@api_view(['GET','POST','DELETE','PUT'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def nodo_handler(request,nodo_id):
    if request.method == 'GET':
        return get_nodo(nodo_id)
    elif request.method == 'POST':
        return post_nodo_child(request,nodo_id)
    elif request.method == 'DELETE':
        return delete_nodo(request,nodo_id)
    elif request.method == 'PUT':
        return put_titolo_nodo(request,nodo_id)

