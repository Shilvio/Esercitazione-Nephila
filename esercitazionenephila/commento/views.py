from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import *
from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from risorsa import views as risorsa_views
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# cerca commenti in basa all'id di una risorsa
def search_commento(commento_id):
    try:
        commenti = Commento.objects.get(id= commento_id)
        return commenti
    except Commento.DoesNotExist:
        return None


# cerca commenti in basa all'id di una risorsa
def search_commenti(risorsa_id):
    try:
        commenti = Commento.objects.filter(risorsa= risorsa_id).all()
        return commenti
    except Commento.DoesNotExist:
        return None

# api handler per generare i commenti
@swagger_auto_schema(
    tags=['commenti'],
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'contenuto': openapi.Schema(type=openapi.TYPE_STRING, default='contenuto test'),
        },
        required=['contenuto']
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
def post_commento(request,nodo_id,risorsa_id):
    risorsa = risorsa_views.search_risorsa(risorsa_id)
    if not risorsa:
        return Response({"details": "Nessuna risorsa da commentare"},status=status.HTTP_404_NOT_FOUND)
    if risorsa.owner.id == request.user.id:
        try:
            if ((not request.data)or(request.data['contenuto'] in [None,''])):
                return Response({"details": "Richeista malformata"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"details": "Richeista malformata"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = CreateCommentoSerializer(data={'risorsa':risorsa.id,'contenuto':request.data['contenuto']})
        if serializer.is_valid():
            serializer.save()
            return Response({"nodo": serializer.data})
        return Response({"details": "Richeista malformata"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"details":"Non autorizzato"}, status=status.HTTP_401_UNAUTHORIZED)

# api handler per eliminare i commenti
@swagger_auto_schema(
    tags=['commenti'],
    method='delete',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'contenuto': openapi.Schema(type=openapi.TYPE_STRING, default='contenuto test'),
        },
        required=['contenuto']
    ),
    responses={
        201: 'Created',
        400: 'Bad Request',
    }
)

# delete commento
@api_view(['DELETE'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_commento(request,nodo_id,risorsa_id,commento_id):

    commento = search_commento(commento_id)
    if commento.risorsa.owner.id == request.user.id:
        if not commento:
            return Response({"details": "Nessun risorsa presente"},status=status.HTTP_404_NOT_FOUND)
        commento.delete()
        return Response({"details": "commento cancellato"})

    else:
        return Response({"details":"Non autorizzato"}, status=status.HTTP_401_UNAUTHORIZED)