from rest_framework.generics import ListAPIView
from .models import Produit
from .serializers import ProduitSerializer


class ProduitListView(ListAPIView):
    """Liste des produits disponibles à la commande (le menu affiché au client)."""
    queryset = Produit.objects.filter(disponible=True)
    serializer_class = ProduitSerializer
