from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Risorsa
from .serializers import *
from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from commento import views as commento_views
from commento import serializers as serializers_commento
from nodo import views as nodo_views
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# valida il ruolo dell'utente per garantire l'accesso alla risorsa, i su possono accedere a tutto
def validate_role(utente,risorsa):
    if risorsa.owner.id == utente.id:
         return True
    elif utente.ruolo == 0  and risorsa.operatore:
        return True
    elif utente.ruolo == 1  and risorsa.responsabile:
        return True
    elif utente.ruolo == 2:
        return True
    else:
        return False

# funzione di ricerca delle risorse usata dai nodi
def search_risorsa_nodo(nodo_id):
    try :
        risorse = Risorsa.objects.filter(nodo=nodo_id).all()
        return risorse
    except Risorsa.DoesNotExist:
        return None

# funzione di ricerca di una risorsa
def search_risorsa(risorsa_id):
    try :
        risorsa = Risorsa.objects.get(id=risorsa_id)
        return risorsa
    except Risorsa.DoesNotExist:
        return None

# funzione get di una risorsa indicata dall'id
def get_risorsa(request,risorsa_id):
    risorsa = search_risorsa(risorsa_id)
    if not risorsa:
            return Response({"details": "Nessun risorsa presente"},status=status.HTTP_404_NOT_FOUND)
    if validate_role(request.user,risorsa):
        serializer = RisorsaSerializer(risorsa, many=False)
        commenti = commento_views.search_commenti(risorsa_id)
        commentiData = serializers_commento.CommentoSerializer(commenti, many=True).data if commenti else None

        return Response({"risorsa": serializer.data, "commenti":commentiData } )
    else:
        return Response({"details":"Non autorizzato"}, status=status.HTTP_401_UNAUTHORIZED)

# funzione delete di una risorsa indicata dall'id
def delete_risorsa(request,risorsa_id):
    risorsa = search_risorsa(risorsa_id)
    if risorsa.owner.id == request.user.id:
        if not risorsa:
            return Response({"details": "Nessun risorsa presente"},status=status.HTTP_404_NOT_FOUND)
        serializer = RisorsaSerializer(risorsa, many=False)
        risorsa.delete()
        return Response({"details": "risorsa "+ str(serializer.data['id']) + " cancellato"})

    else:
        return Response({"details":"Non autorizzato"}, status=status.HTTP_401_UNAUTHORIZED)

# funzione put di una risorsa indicata dall'id
def put_risorsa(request,risorsa_id):
    risorsa = search_risorsa(risorsa_id)
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

# api view handler per postare una risorsa
@swagger_auto_schema(
    tags=['risorse'],
    methods=['post'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'titolo': openapi.Schema(type=openapi.TYPE_STRING, default='titolo test'),
            'contenuto': openapi.Schema(type=openapi.TYPE_STRING, default='contenuto test'),

        },
        required=['titolo','contenuto']
    ),
    responses={
        201: 'Created',
        400: 'Bad Request',
        404: 'Not Found',
        401: 'Unauthorized'
    }
)
@api_view(['POST'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def post_risorsa(request,nodo_id):
    nodo = nodo_views.search_nodo(nodo_id)
    if not nodo:
        return Response({"details": "Nessun nodo presente sul quale caricare la risorsa"},status=status.HTTP_404_NOT_FOUND)
    if nodo.owner.id == request.user.id:
        try:
            if ((not request.data)or(request.data['titolo'] in [None,''])or(request.data['contenuto'] in [None,''])):
                return Response({"details": "Richeista malformata"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"details": "Richeista malformata"}, status=status.HTTP_400_BAD_REQUEST)

        request.data['owner']=request.user.id
        request.data['nodo']= nodo_id
        serializer = CreateRisorsaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"risorsa": serializer.data},status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response({"details": "Richeista malformata"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"details":"Non autorizzato"}, status=status.HTTP_401_UNAUTHORIZED)

# api view handler per operazione get delete e put una risorsa
@swagger_auto_schema(
    tags=['risorse'],
    methods=['get','delete'],
    responses={
        200: 'OK',
        404: 'Not Found',
        401: 'Unauthorized',
    }
)
@swagger_auto_schema(
    tags=['risorse'],
    methods=['put'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'titolo': openapi.Schema(type=openapi.TYPE_STRING, default='titolo test'),
            'contenuto': openapi.Schema(type=openapi.TYPE_STRING, default='contenuto test'),

        },
        required=['titolo','contenuto']
    ),
    responses={
        200: 'Created',
        400: 'Bad Request',
        404: 'Not Found'
    }
)
@api_view(['GET','DELETE','PUT'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def risorsa_id_handler(request,nodo_id,risorsa_id):
    if request.method == 'GET':
        return get_risorsa(request,risorsa_id)
    elif request.method == 'DELETE':
        return delete_risorsa(request,risorsa_id)
    elif request.method == 'PUT':
        return put_risorsa(request,risorsa_id)

# api view handler per generare una risorsa nel nodo padre
@swagger_auto_schema(
    tags=['risorse'],
    methods=['post'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'titolo': openapi.Schema(type=openapi.TYPE_STRING, default='titolo test'),
            'contenuto': openapi.Schema(type=openapi.TYPE_STRING, default='contenuto test'),

        },
        required=['titolo','contenuto']
    ),
    responses={
        201: 'Created',
        400: 'Bad Request',
        404: 'Not Found',
        401: 'Unauthorized'
    }
)
@api_view(['POST'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def post_nuova_risorsa_padre(request,nodo_id):
    padre = nodo_views.search_nodo_padre(nodo_id)
    if not padre:
        return Response({"details": "Nessun nodo padre presente sul quale caricare la risorsa"},status=status.HTTP_404_NOT_FOUND)
    if padre.owner.id == request.user.id:
        try:
            if ((not request.data)or(request.data['titolo'] in [None,''])or(request.data['contenuto'] in [None,''])):
                return Response({"details": "Richeista malformata"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"details": "Richeista malformata"}, status=status.HTTP_400_BAD_REQUEST)

        request.data['owner']=request.user.id
        request.data['nodo']= padre.id
        serializer = CreateRisorsaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"risorsa": serializer.data},status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response({"details": "Richeista malformata"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"details":"Non autorizzato"}, status=status.HTTP_401_UNAUTHORIZED)
