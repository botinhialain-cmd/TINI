from rest_framework.permissions import BasePermission


def role_utilisateur(request):
    """Renvoie le rôle effectif de l'utilisateur connecté, ou None.
    Un superuser (compte admin) est toujours traité comme gérant, même
    sans profil explicite créé."""
    if request.user.is_superuser:
        return "gerant"
    profil = getattr(request.user, "profil", None)
    return profil.role if profil else None


class EstGerant(BasePermission):
    """Autorise uniquement les comptes ayant le rôle 'gerant'."""

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated) and role_utilisateur(request) == "gerant"


class PeutVoirCommandes(BasePermission):
    """
    - Création (POST) : ouverte à tous, c'est le client qui passe commande.
    - Liste des commandes en cours (GET sans ?vue=historique) : réservée
      aux comptes connectés (serveur ou gérant).
    - Historique (GET ?vue=historique) : réservé au gérant uniquement.
    """

    def has_permission(self, request, view):
        if request.method == "POST":
            return True

        if not (request.user and request.user.is_authenticated):
            return False

        if request.query_params.get("vue") == "historique":
            return role_utilisateur(request) == "gerant"

        return True
