"""
Module de notification découplé du reste de l'application.

Le principe : le code métier (création de commande) appelle juste
`notifier_nouvelle_commande(commande)`. Ce module décide COMMENT
notifier (WhatsApp, notifications push mobile) sans que le reste de
l'app n'ait à changer.
"""
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


def notifier_nouvelle_commande(commande):
    """
    Point d'entrée unique appelé à chaque nouvelle commande.
    Chaque canal est indépendant : si l'un échoue (ex: Twilio down),
    les autres sont quand même tentés.
    """
    message = _construire_message(commande)

    try:
        _envoyer_whatsapp(message)
    except Exception:
        logger.exception("Échec de l'envoi WhatsApp pour la commande #%s", commande.id)

    try:
        _envoyer_push(commande, message)
    except Exception:
        logger.exception("Échec de l'envoi push pour la commande #%s", commande.id)


def _construire_message(commande):
    lignes = "\n".join(
        f"- {ligne.quantite} x {ligne.produit.nom} ({ligne.produit.format})"
        for ligne in commande.lignes.all()
    )
    return (
        f"🍺 Nouvelle commande - Table {commande.table.numero}\n"
        f"{lignes}\n"
        f"Total : {commande.total} FCFA"
    )


def _envoyer_whatsapp(message):
    """
    Envoie le message via Twilio (sandbox WhatsApp).
    Nécessite dans settings.py / variables d'env :
    - TWILIO_ACCOUNT_SID
    - TWILIO_AUTH_TOKEN
    - TWILIO_WHATSAPP_FROM  (ex: 'whatsapp:+14155238886' pour le sandbox)
    - GERANTE_WHATSAPP_TO   (ex: 'whatsapp:+2250700000000')
    """
    from twilio.rest import Client

    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    client.messages.create(
        from_=settings.TWILIO_WHATSAPP_FROM,
        to=settings.GERANTE_WHATSAPP_TO,
        body=message,
    )


def _envoyer_push(commande, message_whatsapp):
    """
    Envoie une notification push à tous les appareils mobiles enregistrés
    (app "Tini Gérant"), via le service gratuit d'Expo — aucune clé
    Firebase/Apple à configurer, Expo gère le routage vers iOS/Android.
    """
    import requests
    from comptes.models import PushToken

    jetons = list(PushToken.objects.values_list("token", flat=True))
    if not jetons:
        return

    produits_resume = ", ".join(
        f"{ligne.quantite} {ligne.produit.nom}" for ligne in commande.lignes.all()
    )

    messages = [
        {
            "to": jeton,
            "sound": "default",
            "title": f"Nouvelle commande — Table {commande.table.numero}",
            "body": f"{produits_resume} · {commande.total} FCFA",
            "data": {"commande_id": commande.id},
        }
        for jeton in jetons
    ]

    reponse = requests.post(
        "https://exp.host/--/api/v2/push/send",
        json=messages,
        headers={"Content-Type": "application/json"},
        timeout=10,
    )
    reponse.raise_for_status()
