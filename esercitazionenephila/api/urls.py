from django.urls import path
from . import views

urlpatterns = [
    path('utenti/', views.GetUtente),
    path('risorse/', views.GetRrisorsa)
]
