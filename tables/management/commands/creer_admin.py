"""
Crée un compte superuser à partir de variables d'environnement, sans interaction.
Pratique quand on n'a pas d'accès Shell (ex: plan gratuit Render).

Variables nécessaires :
    DJANGO_SUPERUSER_USERNAME
    DJANGO_SUPERUSER_EMAIL
    DJANGO_SUPERUSER_PASSWORD

Si le compte existe déjà, ne fait rien (sûr à relancer à chaque déploiement).
Si les variables ne sont pas définies, ne fait rien silencieusement (permet de
garder cette commande dans le Procfile en permanence sans risque).
"""
import os
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Crée un superuser depuis des variables d'environnement (non-interactif)."

    def handle(self, *args, **options):
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

        if not username or not password:
            self.stdout.write("Pas de DJANGO_SUPERUSER_* défini — étape ignorée.")
            return

        User = get_user_model()

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f"Superuser '{username}' existe déjà — ignoré."))
            return

        User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' créé avec succès."))
