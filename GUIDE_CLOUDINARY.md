# Guide — Photos permanentes avec Cloudinary

## Pourquoi

Sur le plan gratuit Render, les photos uploadées via l'admin disparaissent
à chaque redéploiement (le disque n'est pas permanent). Cloudinary est un
service gratuit qui stocke les images de façon permanente, à part.

## 1. Créer un compte Cloudinary

1. Va sur https://cloudinary.com/users/register/free
2. Crée un compte (gratuit, aucune carte bancaire requise)
3. Une fois connecté, va sur ton **Dashboard** Cloudinary

## 2. Récupérer ton URL de connexion

Sur le Dashboard, cherche un champ appelé **"API Environment variable"**
ou **"CLOUDINARY_URL"**. Il ressemble à :

```
cloudinary://123456789012345:AbCdEfGhIjKlMnOpQrStUvWxYz@ton-cloud-name
```

Copie cette valeur complète.

## 3. Ajouter la variable sur Render

1. Va sur ton service **TINI** sur Render → **Environment**
2. **Edit** → **+ Add Environment Variable**
3. Key : `CLOUDINARY_URL`
4. Value : colle l'URL copiée
5. **Save, rebuild, and deploy**

## 4. Tester

Une fois redéployé :
1. Va dans l'admin (`/admin/produits/produit/`)
2. Ajoute/modifie une photo sur un produit
3. Redéploie une nouvelle fois (par exemple en repoussant un petit changement)
4. Vérifie que la photo est toujours là — c'est le vrai test de la permanence

## Note

Sans cette variable, tout continue à fonctionner exactement comme avant
(photos stockées localement, temporaires). Cloudinary ne s'active que si
`CLOUDINARY_URL` est définie.
