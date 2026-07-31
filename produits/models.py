from django.db import models


class Produit(models.Model):
    """
    Un produit vendable (bière pour le MVP).
    La catégorie est déjà prévue pour accueillir plats/softs plus tard sans tout casser.
    """
    CATEGORIE_CHOICES = [
        ("biere", "Bière"),
        ("soft", "Boisson sans alcool"),
        ("plat", "Plat"),
    ]

    nom = models.CharField(max_length=100)
    categorie = models.CharField(max_length=20, choices=CATEGORIE_CHOICES, default="biere")
    format = models.CharField(max_length=20, blank=True, help_text="Ex: 33cl, 65cl")
    prix = models.PositiveIntegerField(help_text="Prix en FCFA")
    disponible = models.BooleanField(default=True)
    photo = models.ImageField(upload_to="produits/", blank=True, null=True)

    class Meta:
        ordering = ["categorie", "nom"]

    def __str__(self):
        return f"{self.nom} ({self.format}) - {self.prix} FCFA"
