"""
Charge une liste de bières courantes en Côte d'Ivoire, avec des prix indicatifs.
Pratique pour peupler rapidement le menu en phase de test.

Usage :
    python manage.py charger_bieres

Les prix sont indicatifs (voir discussion) — à ajuster ensuite dans l'admin
selon les vrais tarifs pratiqués.
"""
from django.core.management.base import BaseCommand
from produits.models import Produit

BIERES = [
    {"nom": "Bock", "format": "33cl", "prix": 700},
    {"nom": "Flag", "format": "33cl", "prix": 700},
    {"nom": "Beaufort", "format": "33cl", "prix": 800},
    {"nom": "Ivoire", "format": "33cl", "prix": 900},
    {"nom": "Heineken", "format": "33cl", "prix": 1300},
    {"nom": "Desperados", "format": "33cl", "prix": 1300},
]


class Command(BaseCommand):
    help = "Charge une liste de bières courantes (Côte d'Ivoire) avec prix indicatifs."

    def handle(self, *args, **options):
        crees = 0
        for biere in BIERES:
            _, cree = Produit.objects.get_or_create(
                nom=biere["nom"],
                format=biere["format"],
                defaults={"categorie": "biere", "prix": biere["prix"], "disponible": True},
            )
            if cree:
                crees += 1
                self.stdout.write(self.style.SUCCESS(f"Créé : {biere['nom']} ({biere['prix']} FCFA)"))
            else:
                self.stdout.write(self.style.WARNING(f"Déjà présent : {biere['nom']} — ignoré"))

        self.stdout.write(self.style.SUCCESS(f"\n{crees} bière(s) ajoutée(s)."))
