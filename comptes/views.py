from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import PushToken


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


class EnregistrerPushTokenView(APIView):
    """
    Enregistre (ou réattribue) un jeton de notification push Expo pour
    l'utilisateur connecté, appelé par l'application mobile au démarrage
    et après connexion.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        jeton = request.data.get("token", "").strip()
        if not jeton:
            return Response({"detail": "Le champ 'token' est requis."}, status=status.HTTP_400_BAD_REQUEST)

        # Un même jeton d'appareil ne doit être rattaché qu'à un seul compte à la fois
        # (ex: un téléphone partagé où un autre membre du personnel se connecte ensuite).
        PushToken.objects.update_or_create(
            token=jeton,
            defaults={"user": request.user},
        )
        return Response({"detail": "Jeton enregistré."}, status=status.HTTP_200_OK)
