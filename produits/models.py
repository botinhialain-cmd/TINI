import os
from django.db import models


def _stockage_photos():
    """
    Retourne l'instance de stockage à utiliser pour les photos produits.
    Résolu directement (plutôt que via le mécanisme global storages['default']
    de Django) pour éviter un bug de résolution rencontré en production.
    """
    if os.environ.get('CLOUDINARY_URL'):
        from cloudinary_storage.storage import MediaCloudinaryStorage
        return MediaCloudinaryStorage()
    from django.core.files.storage import FileSystemStorage
    return FileSystemStorage()


class Categorie(models.Model):
    """
    Une catégorie de produits (Bière, Vin, Cocktail...), gérable librement
    depuis l'admin — plus besoin de toucher au code pour en ajouter une.
    """
    nom = models.CharField(max_length=50, unique=True, help_text="Ex: Bières, Vins, Cocktails...")
    ordre = models.PositiveIntegerField(
        default=0,
        help_text="Détermine l'ordre d'affichage des sections sur le menu client (plus petit = affiché en premier)",
    )
    actif = models.BooleanField(
        default=True,
        help_text="Décocher pour masquer temporairement toute la catégorie du menu client, sans la supprimer",
    )

    class Meta:
        ordering = ["ordre", "nom"]
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"

    def __str__(self):
        return self.nom


class Produit(models.Model):
    """
    Un produit vendable (bière, vin, cocktail, etc.).
    """
    nom = models.CharField(max_length=100)
    categorie = models.ForeignKey(Categorie, on_delete=models.PROTECT, related_name="produits")
    format = models.CharField(max_length=20, blank=True, help_text="Ex: 33cl, 65cl")
    prix = models.PositiveIntegerField(help_text="Prix de vente en FCFA")
    cout = models.PositiveIntegerField(
        default=0,
        help_text="Coût d'achat unitaire en FCFA — sert à calculer le bénéfice dans l'onglet 'Bénéfice' du tableau de bord",
    )
    disponible = models.BooleanField(default=True)
    photo = models.ImageField(upload_to="produits/", blank=True, null=True, storage=_stockage_photos)

    class Meta:
        ordering = ["categorie__ordre", "nom"]

    def __str__(self):
        return f"{self.nom} ({self.format}) - {self.prix} FCFA"
