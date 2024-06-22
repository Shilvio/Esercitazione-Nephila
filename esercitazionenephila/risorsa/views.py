from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Risorsa
from .serializers import *

# Create your views here.

def searchRisorsa(risorsa_id):
    try :
        risorsa = Risorsa.objects.get(id=risorsa_id)
        return risorsa
    except Risorsa.DoesNotExist:
        return None

@api_view(['GET'])
def GetRisorsa(request):
    risorsa = searchRisorsa(risorsa_id)
    if not risorsa:
        return Response({"details": "Nessun risorsa presente"},status=status.HTTP_404_NOT_FOUND)
    serializer = RisorsaSerializer(risorsa, many=False)
    figliSerializer = RisorsaSerializer(figli, many=True)
    return Response({"risorsa": serializer.data, "figli":figliSerializer.data, "risorse":figliSerializer.data} )