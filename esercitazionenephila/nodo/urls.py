from django.urls import path
from nodo import views


urlpatterns = [
    path('nodi', views.post_nodo_root),
    path('nodi/<int:nodo_id>', views.nodo_handler),
    path('nodi/<int:nodo_id>/padre', views.post_nuovo_child_in_padre),
]
