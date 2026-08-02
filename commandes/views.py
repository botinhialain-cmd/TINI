import logging

from django.db.models import Sum, F
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from tables.models import Table
from produits.models import Produit
from notifications.services import notifier_nouvelle_commande
from comptes.permissions import EstGerant, PeutVoirCommandes
from .models import Commande, LigneCommande
from .serializers import CommandeSerializer, CommandeCreationSerializer


class CommandeCreationView(APIView):
    """
    Point d'entrée unique du parcours client : reçoit le panier, crée la
    commande + ses lignes, puis déclenche la notification WhatsApp.
    GET : liste des commandes récentes, utilisée par le tableau de bord
    du personnel pour suivre les commandes en direct. L'historique
    (?vue=historique) est réservé au rôle gérant (voir PeutVoirCommandes).
    """

    permission_classes = [PeutVoirCommandes]

    def get(self, request):
        vue = request.query_params.get("vue")

        if vue == "historique":
            commandes = Commande.objects.all().order_by("-date_creation")[:100]
        else:
            commandes = Commande.objects.exclude(statut="servie").order_by("-date_creation")[:50]

        sortie = CommandeSerializer(commandes, many=True)
        return Response(sortie.data)

    def post(self, request):
        entree = CommandeCreationSerializer(data=request.data)
        entree.is_valid(raise_exception=True)
        donnees = entree.validated_data

        table = get_object_or_404(Table, code_qr=donnees["table_code_qr"], active=True)
        commande = Commande.objects.create(table=table)

        for ligne in donnees["lignes"]:
            produit = get_object_or_404(Produit, id=ligne["produit_id"], disponible=True)
            LigneCommande.objects.create(
                commande=commande,
                produit=produit,
                quantite=ligne["quantite"],
                prix_unitaire=produit.prix,
            )

        # La notif ne doit jamais faire échouer la commande si Twilio a un souci,
        # mais on garde une trace pour pouvoir déboguer.
        try:
            notifier_nouvelle_commande(commande)
        except Exception:
            logging.getLogger(__name__).exception(
                "Échec de la notification WhatsApp pour la commande #%s", commande.id
            )

        sortie = CommandeSerializer(commande)
        return Response(sortie.data, status=status.HTTP_201_CREATED)


class CommandeDetailView(RetrieveAPIView):
    """Permet au client de suivre le statut de sa commande."""
    queryset = Commande.objects.all()
    serializer_class = CommandeSerializer


class CommandeStatutView(APIView):
    """Permet au personnel connecté de faire avancer le statut d'une commande."""

    permission_classes = [IsAuthenticated]

    STATUTS_VALIDES = {"recue", "en_preparation", "servie", "annulee"}

    def patch(self, request, pk):
        commande = get_object_or_404(Commande, pk=pk)
        nouveau_statut = request.data.get("statut")

        if nouveau_statut not in self.STATUTS_VALIDES:
            return Response(
                {"detail": f"Statut invalide. Valeurs possibles : {sorted(self.STATUTS_VALIDES)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        commande.statut = nouveau_statut
        champs_modifies = ["statut"]

        if nouveau_statut == "servie":
            commande.servi_par = request.user
            champs_modifies.append("servi_par")

        commande.save(update_fields=champs_modifies)

        sortie = CommandeSerializer(commande)
        return Response(sortie.data)


class CommandePaiementView(APIView):
    """
    Permet au personnel connecté de marquer une commande comme payée ou non,
    indépendamment de son statut de préparation (le client peut payer
    avant, pendant ou après avoir été servi, ou régler plusieurs
    commandes d'un coup en fin de visite).
    """

    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        commande = get_object_or_404(Commande, pk=pk)
        paye = request.data.get("paye")

        if not isinstance(paye, bool):
            return Response(
                {"detail": "Le champ 'paye' doit être un booléen (true/false)."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        commande.paye = paye
        commande.save(update_fields=["paye"])

        sortie = CommandeSerializer(commande)
        return Response(sortie.data)


class CommandeStatsView(APIView):
    """
    Récapitulatif des ventes : quantité et montant total par produit,
    calculé uniquement sur les commandes marquées 'servie' (les seules
    ventes réellement finalisées). Réservé au rôle gérant.
    """

    permission_classes = [EstGerant]

    def get(self, request):
        lignes = (
            LigneCommande.objects.filter(commande__statut="servie")
            .values("produit__nom")
            .annotate(
                quantite_totale=Sum("quantite"),
                montant_total=Sum(F("quantite") * F("prix_unitaire")),
            )
            .order_by("-montant_total")
        )

        produits = [
            {
                "nom": ligne["produit__nom"],
                "quantite": ligne["quantite_totale"],
                "montant": ligne["montant_total"],
            }
            for ligne in lignes
        ]

        total_general = sum(p["montant"] for p in produits)

        return Response({"produits": produits, "total_general": total_general})
