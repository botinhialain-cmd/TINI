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


class PushToken(models.Model):
    """
    Jeton de notification push (Expo) enregistré par l'application mobile
    d'un membre du personnel, pour lui envoyer une alerte à chaque nouvelle
    commande même si l'app est fermée.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="push_tokens")
    token = models.CharField(max_length=200, unique=True, help_text="Jeton ExponentPushToken[...] fourni par l'app")
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Push token de {self.user.username}"
