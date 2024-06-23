from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import *
from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from risorsa import views as risorsa_views
# Create your views here.

def search_commenti(risorsa_id):
    try:
        commenti = Commento.objects.filter(risorsa= risorsa_id).all()
        return commenti
    except Commento.DoesNotExist:
        return None

@api_view(['POST'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def post_commento(request,nodo_id,risorsa_id):
    risorsa = risorsa_views.search_risorsa(risorsa_id)
    if not risorsa:
        return Response({"details": "Nessun nodo padre presente sul quale caricare la risorsa"},status=status.HTTP_404_NOT_FOUND)
    if risorsa.owner.id == request.user.id:
        if ((not request.data)or(request.data['contenuto'] in [None,''])):
            return Response({"details": "Richeista malformata"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = CreateCommentoSerializer(data={'risorsa':risorsa.id,'contenuto':request.data['contenuto']})
        if serializer.is_valid():
            serializer.save()
            return Response({"nodo": serializer.data})
        return Response({"details": "Richeista malformata"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"details":"Non autorizzato"}, status=status.HTTP_401_UNAUTHORIZED)
