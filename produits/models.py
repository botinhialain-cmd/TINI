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
    photo = models.ImageField(upload_to="produits/", blank=True, null=True, storage=_stockage_photos)

    class Meta:
        ordering = ["categorie", "nom"]

    def __str__(self):
        return f"{self.nom} ({self.format}) - {self.prix} FCFA"
