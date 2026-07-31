from rest_framework import serializers
from .models import Commande, LigneCommande
from produits.models import Produit
from produits.serializers import ProduitSerializer


class LigneCommandeLectureSerializer(serializers.ModelSerializer):
    produit = ProduitSerializer(read_only=True)

    class Meta:
        model = LigneCommande
        fields = ["id", "produit", "quantite", "prix_unitaire", "sous_total"]


class LigneCommandeEcritureSerializer(serializers.Serializer):
    """Utilisé uniquement en entrée lors de la création d'une commande."""
    produit_id = serializers.IntegerField()
    quantite = serializers.IntegerField(min_value=1)


class CommandeSerializer(serializers.ModelSerializer):
    lignes = LigneCommandeLectureSerializer(many=True, read_only=True)
    total = serializers.ReadOnlyField()
    table_numero = serializers.IntegerField(source="table.numero", read_only=True)

    class Meta:
        model = Commande
        fields = ["id", "table", "table_numero", "statut", "date_creation", "lignes", "total"]
        read_only_fields = ["statut", "date_creation"]


class CommandeCreationSerializer(serializers.Serializer):
    """Serializer d'entrée pour créer une commande depuis le menu client."""
    table_code_qr = serializers.UUIDField()
    lignes = LigneCommandeEcritureSerializer(many=True)

    def validate_lignes(self, lignes):
        if not lignes:
            raise serializers.ValidationError("La commande doit contenir au moins un produit.")
        return lignes
