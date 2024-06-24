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
# Create your views here.

def search_commenti(risorsa_id):
    try:
        commenti = Commento.objects.filter(risorsa= risorsa_id).all()
        return commenti
    except Commento.DoesNotExist:
        return None


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
        serializer = CreateCommentoSerializer(data={'risorsa':risorsa.id,'contenuto':request.data['contenuto']},status=status.HTTP_201_CREATED)
        if serializer.is_valid():
            serializer.save()
            return Response({"nodo": serializer.data})
        return Response({"details": "Richeista malformata"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"details":"Non autorizzato"}, status=status.HTTP_401_UNAUTHORIZED)
