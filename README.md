# Tini Backend - MVP

## Installation

```bash
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install django djangorestframework qrcode pillow twilio
python manage.py migrate
python manage.py createsuperuser   # pour accéder à /admin/
python manage.py runserver
```

## Configuration WhatsApp (Twilio)

Variables d'environnement à définir avant de lancer le serveur (sandbox Twilio) :

```bash
export TWILIO_ACCOUNT_SID="xxx"
export TWILIO_AUTH_TOKEN="xxx"
export TWILIO_WHATSAPP_FROM="whatsapp:+14155238886"   # numéro sandbox Twilio
export GERANTE_WHATSAPP_TO="whatsapp:+225XXXXXXXXXX"  # numéro de ta cliente
```

Tant que ces variables ne sont pas définies, les commandes fonctionnent quand même
(la notif échoue silencieusement et l'erreur est juste loguée) — utile pour développer
sans dépendre de Twilio.

## Endpoints API

| Méthode | URL | Description |
|---|---|---|
| GET | `/api/produits/` | Liste des produits disponibles |
| GET | `/api/tables/<code_qr>/` | Détail d'une table via son QR code |
| POST | `/api/commandes/` | Créer une commande |
| GET | `/api/commandes/<id>/` | Suivre le statut d'une commande |

### Exemple de création de commande

```bash
curl -X POST http://127.0.0.1:8000/api/commandes/ \
  -H "Content-Type: application/json" \
  -d '{
    "table_code_qr": "UUID_DE_LA_TABLE",
    "lignes": [
      {"produit_id": 1, "quantite": 2}
    ]
  }'
```

## Admin

Accessible sur `/admin/` — permet à toi ou ta cliente d'ajouter/modifier
les produits (prix, dispo) et les tables sans toucher au code.

## Prochaines étapes (dans l'ordre)

1. Génération des QR codes physiques par table
2. Frontend React (scan → menu → panier → validation)
3. Configurer Twilio en vrai (sandbox puis production)
4. Vue dashboard simple pour suivre les commandes en cours
