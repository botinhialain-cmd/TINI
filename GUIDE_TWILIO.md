# Configurer Twilio WhatsApp (sandbox) — Guide pas à pas

## 1. Créer un compte Twilio

Va sur https://www.twilio.com/try-twilio et crée un compte gratuit.
Tu reçois un crédit d'essai (~15$), largement suffisant pour tester.

## 2. Activer le sandbox WhatsApp

1. Dans le tableau de bord Twilio, va dans **Messaging → Try it out → Send a WhatsApp message**
2. Twilio te donne un numéro sandbox (ex: `+1 415 523 8886`) et un code du type `join xxx-xxx`
3. **Ton amie doit envoyer ce message** depuis SON WhatsApp personnel vers ce numéro sandbox, une seule fois
   (ex: elle envoie "join chien-bleu" au +1 415 523 8886)
4. Une fois fait, Twilio peut lui envoyer des messages automatiques

⚠️ Le sandbox expire après 72h d'inactivité — il faudra refaire le "join" si vous ne testez pas pendant plusieurs jours. C'est une limite du sandbox uniquement, pas de la production.

## 3. Récupérer tes clés API

Sur le tableau de bord principal Twilio (https://console.twilio.com), tu trouveras :
- **Account SID** (commence par `AC...`)
- **Auth Token** (clique sur "show" pour le révéler)

## 4. Configurer le backend

Dans ton terminal, avant de lancer `python manage.py runserver`, exporte ces variables :

```bash
export TWILIO_ACCOUNT_SID="AC_ton_sid_ici"
export TWILIO_AUTH_TOKEN="ton_token_ici"
export TWILIO_WHATSAPP_FROM="whatsapp:+14155238886"
export GERANTE_WHATSAPP_TO="whatsapp:+225XXXXXXXXXX"
```

Remplace le numéro de `GERANTE_WHATSAPP_TO` par le vrai numéro WhatsApp de ton amie
(celui qui a fait le "join"), au format international avec le `+`.

**Astuce pratique** : plutôt que de taper ces `export` à chaque fois, crée un fichier
`lancer_serveur.sh` à la racine du projet :

```bash
#!/bin/bash
export TWILIO_ACCOUNT_SID="AC_ton_sid_ici"
export TWILIO_AUTH_TOKEN="ton_token_ici"
export TWILIO_WHATSAPP_FROM="whatsapp:+14155238886"
export GERANTE_WHATSAPP_TO="whatsapp:+225XXXXXXXXXX"
python manage.py runserver
```

Puis lance juste `bash lancer_serveur.sh`.

⚠️ **Ne mets jamais ce fichier sur GitHub** (ajoute-le à `.gitignore`) — il contient des secrets.

## 5. Tester

Passe une commande depuis le frontend (ou via curl). Ton amie doit recevoir un message
WhatsApp du type :

```
🍺 Nouvelle commande - Table 4
- 2 x Bock (33cl)
Total : 1400 FCFA
```

## 6. Pour la production plus tard

Le sandbox suffit pour valider le concept avec ta première cliente. Le jour où tu veux
un vrai numéro dédié (pas de "join" à refaire, pas de limite d'inactivité), il faudra
passer par la validation Meta Business — voir la conversation précédente pour le détail
de cette démarche.
