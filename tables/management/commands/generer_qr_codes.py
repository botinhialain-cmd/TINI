"""
Génère un QR code (image PNG) par table, prêt à imprimer.

Usage :
    python manage.py generer_qr_codes --url-frontend https://ton-domaine.com

En dev, sans argument, utilise http://localhost:5173 par défaut.
Les images sont créées dans le dossier qr_codes/ à la racine du projet.
"""
import os
import qrcode
from django.core.management.base import BaseCommand
from tables.models import Table


class Command(BaseCommand):
    help = "Génère un QR code PNG par table, pointant vers le frontend."

    def add_arguments(self, parser):
        parser.add_argument(
            "--url-frontend",
            type=str,
            default="http://localhost:5173",
            help="URL de base du frontend (sans slash final), ex: https://tini-monbar.com",
        )
        parser.add_argument(
            "--dossier",
            type=str,
            default="qr_codes",
            help="Dossier de sortie pour les images générées",
        )

    def handle(self, *args, **options):
        url_frontend = options["url_frontend"].rstrip("/")
        dossier = options["dossier"]
        os.makedirs(dossier, exist_ok=True)

        tables = Table.objects.filter(active=True)
        if not tables.exists():
            self.stdout.write(self.style.WARNING("Aucune table active trouvée. Rien à générer."))
            return

        for table in tables:
            lien = f"{url_frontend}/?table={table.code_qr}"
            image = qrcode.make(lien)
            chemin = os.path.join(dossier, f"table_{table.numero}.png")
            image.save(chemin)
            self.stdout.write(self.style.SUCCESS(f"Table {table.numero} → {chemin} ({lien})"))

        self.stdout.write(self.style.SUCCESS(f"\n{tables.count()} QR code(s) généré(s) dans '{dossier}/'."))
