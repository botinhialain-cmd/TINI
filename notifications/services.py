"""
Module de notification découplé du reste de l'application.

Le principe : le code métier (création de commande) appelle juste
`notifier_nouvelle_commande(commande)`. Ce module décide COMMENT
notifier (WhatsApp aujourd'hui, push/dashboard demain) sans que le
reste de l'app n'ait à changer.
"""
from django.conf import settings


def notifier_nouvelle_commande(commande):
    """Point d'entrée unique appelé à chaque nouvelle commande."""
    message = _construire_message(commande)
    _envoyer_whatsapp(message)


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
