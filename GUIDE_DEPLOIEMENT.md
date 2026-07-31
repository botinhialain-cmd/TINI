# Guide de déploiement — Tini MVP

Objectif : rendre ton app accessible depuis n'importe quel téléphone, pas
seulement ton ordinateur. On déploie le backend sur **Render** et le
frontend sur **Vercel** — les deux ont un plan gratuit suffisant pour un MVP.

---

## Étape 1 — Pousser le backend sur GitHub

Dans le dossier `tini_backend` :

```bash
git init
git add .
git commit -m "Version initiale du backend Tini"
```

Crée un nouveau dépôt sur https://github.com/new (nom suggéré : `tini-backend`),
**ne coche aucune case** (pas de README, pas de .gitignore — on les a déjà).

GitHub t'affichera des commandes du type :
```bash
git remote add origin https://github.com/TON_USERNAME/tini-backend.git
git branch -M main
git push -u origin main
```
Copie-les depuis ta page GitHub et exécute-les.

---

## Étape 2 — Déployer le backend sur Render

1. Va sur https://render.com et crée un compte (tu peux te connecter directement avec GitHub)
2. Clique sur **New +** → **Web Service**
3. Connecte ton dépôt `tini-backend`
4. Render détecte Python automatiquement. Vérifie/renseigne :
   - **Build Command** : `pip install -r requirements.txt`
   - **Start Command** : laisse vide (le `Procfile` s'en charge automatiquement)
   - **Instance Type** : Free
5. Dans **Environment Variables**, ajoute :

| Clé | Valeur |
|---|---|
| `DJANGO_SECRET_KEY` | une longue chaîne aléatoire (ex: génère-en une sur https://djecrety.ir) |
| `DJANGO_DEBUG` | `False` |
| `DJANGO_ALLOWED_HOSTS` | `ton-service.onrender.com` (Render te donne cette URL après création) |
| `CORS_ALLOWED_ORIGINS` | laisse vide pour l'instant, on le complétera à l'étape 4 |

6. Clique sur **Create Web Service**. Le déploiement prend 2-5 minutes.

7. Une fois déployé, va dans l'onglet **Shell** de Render (ou en local via `render ssh` si tu préfères), et lance une fois :
```bash
python manage.py createsuperuser
```
Pour pouvoir accéder à `/admin/` en ligne et créer tes tables/produits.

**Note ton URL Render** (ex: `https://tini-backend-xxxx.onrender.com`) — tu en auras besoin à l'étape 4.

⚠️ Le plan gratuit Render "s'endort" après 15 min d'inactivité et met ~30-60 secondes
à se réveiller au premier appel. Pour un MVP de test, c'est acceptable ; si ça
devient gênant plus tard, il existe des plans payants sans ce comportement.

---

## Étape 3 — Pousser le frontend sur GitHub

Dans le dossier `tini_frontend` :

```bash
git init
git add .
git commit -m "Version initiale du frontend Tini"
```

Crée un nouveau dépôt sur GitHub (nom suggéré : `tini-frontend`), puis :
```bash
git remote add origin https://github.com/TON_USERNAME/tini-frontend.git
git branch -M main
git push -u origin main
```

---

## Étape 4 — Déployer le frontend sur Vercel

1. Va sur https://vercel.com et connecte-toi avec GitHub
2. Clique sur **Add New** → **Project**
3. Sélectionne ton dépôt `tini-frontend`
4. Vercel détecte Vite automatiquement, aucun réglage à changer
5. Avant de déployer, ajoute une variable d'environnement :

| Clé | Valeur |
|---|---|
| `VITE_API_URL` | l'URL Render de ton backend (ex: `https://tini-backend-xxxx.onrender.com`) |

6. Clique sur **Deploy**. Ça prend 1-2 minutes.

Vercel te donne une URL du type `https://tini-frontend-xxxx.vercel.app` — **c'est le
lien que ta cliente et ses clients utiliseront**.

---

## Étape 5 — Reconnecter le backend au frontend (CORS)

Retourne sur Render → ton service backend → **Environment** → modifie :

| Clé | Valeur |
|---|---|
| `CORS_ALLOWED_ORIGINS` | `https://tini-frontend-xxxx.vercel.app` (ton URL Vercel exacte) |

Sauvegarde — Render redéploie automatiquement (1-2 min).

---

## Étape 6 — Régénérer les QR codes avec la vraie URL

Toujours utile de le faire en local, pointant vers Vercel :

```bash
python manage.py generer_qr_codes --url-frontend https://tini-frontend-xxxx.vercel.app
```

Les images générées dans `qr_codes/` sont maintenant les vraies, à imprimer.

---

## Vérification finale

1. Ouvre `https://tini-backend-xxxx.onrender.com/admin/` → connecte-toi → crée tes
   tables et produits (comme tu l'as fait en local)
2. Scanne un des QR codes fraîchement générés **avec ton téléphone** (plus besoin
   d'être sur le même réseau que ton ordinateur — ça marche depuis n'importe où)
3. Passe une commande de test → vérifie qu'elle apparaît dans l'admin

Si tout ça fonctionne, ton MVP est officiellement testable en conditions réelles
chez ta cliente.

---

## En cas de blocage

- **Erreur CORS dans la console navigateur** → vérifie que `CORS_ALLOWED_ORIGINS`
  sur Render correspond exactement à l'URL Vercel (sans slash final)
- **"DisallowedHost" côté Django** → vérifie `DJANGO_ALLOWED_HOSTS` sur Render
- **Le site met du temps à charger la première fois** → normal, c'est le plan
  gratuit Render qui se réveille
