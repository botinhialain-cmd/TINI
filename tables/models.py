import uuid
from django.db import models


class Table(models.Model):
    """Une table physique de l'établissement, identifiée par un QR code unique."""
    numero = models.PositiveIntegerField(unique=True, help_text="Numéro affiché sur la table (ex: 4)")
    code_qr = models.UUIDField(default=uuid.uuid4, editable=False, unique=True,
                                help_text="Identifiant unique utilisé dans l'URL du QR code")
    active = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["numero"]

    def __str__(self):
        return f"Table {self.numero}"
