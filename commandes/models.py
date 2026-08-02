from django.conf import settings
from django.db import models
from tables.models import Table
from produits.models import Produit


class Commande(models.Model):
    STATUT_CHOICES = [
        ("recue", "Reçue"),
        ("en_preparation", "En préparation"),
        ("servie", "Servie"),
        ("annulee", "Annulée"),
    ]

    table = models.ForeignKey(Table, on_delete=models.PROTECT, related_name="commandes")
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default="recue")
    date_creation = models.DateTimeField(auto_now_add=True)
    date_maj = models.DateTimeField(auto_now=True)
    servi_par = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="commandes_servies",
        help_text="Membre du personnel ayant marqué la commande comme servie",
    )

    class Meta:
        ordering = ["-date_creation"]

    def __str__(self):
        return f"Commande #{self.id} - Table {self.table.numero} ({self.statut})"

    @property
    def total(self):
        return sum(ligne.sous_total for ligne in self.lignes.all())


class LigneCommande(models.Model):
    """Une ligne d'une commande : un produit + une quantité."""
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE, related_name="lignes")
    produit = models.ForeignKey(Produit, on_delete=models.PROTECT)
    quantite = models.PositiveIntegerField(default=1)
    prix_unitaire = models.PositiveIntegerField(help_text="Prix au moment de la commande (historique)")

    def __str__(self):
        return f"{self.quantite} x {self.produit.nom}"

    @property
    def sous_total(self):
        return self.quantite * self.prix_unitaire
