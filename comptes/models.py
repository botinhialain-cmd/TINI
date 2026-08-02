from django.contrib.auth.models import User
from django.db import models


class Profil(models.Model):
    """
    Étend le compte utilisateur Django standard avec un rôle métier.
    - serveur : voit et fait avancer les commandes en cours
    - gerant : voit les commandes en cours + l'historique + les statistiques
    """

    ROLE_SERVEUR = "serveur"
    ROLE_GERANT = "gerant"
    ROLE_CHOICES = [
        (ROLE_SERVEUR, "Serveur"),
        (ROLE_GERANT, "Gérant"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profil")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_SERVEUR)

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"
