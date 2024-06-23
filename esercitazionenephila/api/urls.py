from django.urls import path,include

from utente import views as views_utente
from risorsa import views as views_risorsa
from nodo import views as views_nodo
from commento import views as views_commento


from drf_yasg import openapi
from drf_yasg.views import get_schema_view


swagger_view = get_schema_view(
    openapi.Info(
        title="Post API",
        default_version='1.0.0',
        description="Webapi nodi-risorse per Nephila"
    ),
    public=True,
)


urlpatterns = [
    # path utenti
    path('', include('utente.urls')),

    #path nodi
    path('', include('nodo.urls')),


    #path risorse
    path('', include('risorsa.urls')),

    #path commenti
    path('', include('commento.urls')),

    #path swagger per docu
    path('swagger', swagger_view.with_ui('swagger',cache_timeout=0), name="swagger_schema"),
    path('redoc', swagger_view.with_ui('redoc', cache_timeout=0), name='schema-redoc')
]
