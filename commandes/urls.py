from django.urls import path
from .views import CommandeCreationView, CommandeDetailView, CommandeStatutView

urlpatterns = [
    path("", CommandeCreationView.as_view(), name="commande-creation"),
    path("<int:pk>/", CommandeDetailView.as_view(), name="commande-detail"),
    path("<int:pk>/statut/", CommandeStatutView.as_view(), name="commande-statut"),
]
