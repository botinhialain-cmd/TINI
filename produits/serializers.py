from rest_framework import serializers
from .models import Produit, Categorie


class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = ["id", "nom", "ordre"]


class ProduitSerializer(serializers.ModelSerializer):
    categorie = CategorieSerializer(read_only=True)

    class Meta:
        model = Produit
        fields = ["id", "nom", "categorie", "format", "prix", "disponible", "photo"]
