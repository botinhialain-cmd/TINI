from django.contrib import admin
from django.contrib import messages
from django.db import connection

from .models import Commande, LigneCommande


class LigneCommandeInline(admin.TabularInline):
    model = LigneCommande
    extra = 0
    readonly_fields = ["prix_unitaire", "cout_unitaire"]


@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = ["id", "table", "statut", "total", "date_creation"]
    list_filter = ["statut"]
    inlines = [LigneCommandeInline]
    actions = ["reinitialiser_commandes_test"]

    @admin.action(description="⚠️ Réinitialiser toutes les commandes de test")
    def reinitialiser_commandes_test(self, request, queryset):
        # L'action est volontairement globale :
        # elle supprime toutes les commandes et toutes leurs lignes.
        LigneCommande.objects.all().delete()
        Commande.objects.all().delete()

        # Remet les séquences PostgreSQL à 1.
        # La prochaine commande et la prochaine ligne auront donc l'ID 1.
        if connection.vendor == "postgresql":
            with connection.cursor() as cursor:
                cursor.execute(
                    "ALTER SEQUENCE commandes_commande_id_seq RESTART WITH 1;"
                )
                cursor.execute(
                    "ALTER SEQUENCE commandes_lignecommande_id_seq RESTART WITH 1;"
                )

        self.message_user(
            request,
            "Toutes les commandes de test ont été supprimées. "
            "La numérotation repartira à 1.",
            level=messages.SUCCESS,
        )
