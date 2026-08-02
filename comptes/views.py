from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView


class ConnexionView(APIView):
    """Point d'entrée de connexion pour le personnel (serveur/gérant)."""

    def post(self, request):
        username = request.data.get("username", "")
        password = request.data.get("password", "")

        utilisateur = authenticate(request, username=username, password=password)
        if utilisateur is None:
            return Response(
                {"detail": "Identifiants incorrects."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        token, _ = Token.objects.get_or_create(user=utilisateur)

        if utilisateur.is_superuser:
            role = "gerant"
        else:
            profil = getattr(utilisateur, "profil", None)
            role = profil.role if profil else None

        return Response({"token": token.key, "role": role, "username": utilisateur.username})
