from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Risorsa
from .serializers import *

# Create your views here.
@api_view(['GET'])
def GetRisorsa(req):
    risorsa = Risorsa.objects.all()
    serializer = RisorsaSerializer(risorsa, many = True)
    return Response(serializer.data)