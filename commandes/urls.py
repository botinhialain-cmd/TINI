from django.urls import path
from .views import (
    CommandeCreationView, CommandeDetailView, CommandeStatutView,
    CommandeStatsView, CommandePaiementView, CommandeBeneficeView,
)

urlpatterns = [
    path("", CommandeCreationView.as_view(), name="commande-creation"),
    path("stats/", CommandeStatsView.as_view(), name="commande-stats"),
    path("benefices/", CommandeBeneficeView.as_view(), name="commande-benefices"),
    path("<int:pk>/", CommandeDetailView.as_view(), name="commande-detail"),
    path("<int:pk>/statut/", CommandeStatutView.as_view(), name="commande-statut"),
    path("<int:pk>/paiement/", CommandePaiementView.as_view(), name="commande-paiement"),
]
