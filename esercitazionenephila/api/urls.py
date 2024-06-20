from django.urls import path
from utente import views as views_utente
from risorsa import views as views_risorsa



from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path utenti
    path('register/', views_utente.register),
    path('login/', views_utente.login),
    #path risorse
    path('risorse/', views_risorsa.GetRisorsa),
]
