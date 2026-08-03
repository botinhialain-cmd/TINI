import django.db.models.deletion
from django.db import migrations, models


ANCIENNES_CATEGORIES = [
    ("biere", "Bière", 1),
    ("vin", "Vin", 2),
    ("cocktail", "Cocktail", 3),
    ("spiritueux", "Spiritueux", 4),
    ("energisante", "Boisson énergisante", 5),
    ("soft", "Soft / Sans alcool", 6),
    ("plat", "Plat", 7),
]


def migrer_donnees_vers_categories(apps, schema_editor):
    Produit = apps.get_model("produits", "Produit")
    Categorie = apps.get_model("produits", "Categorie")

    correspondance = {}
    for code, nom, ordre in ANCIENNES_CATEGORIES:
        categorie, _ = Categorie.objects.get_or_create(nom=nom, defaults={"ordre": ordre})
        correspondance[code] = categorie

    # Filet de sécurité : couvre aussi d'anciens codes non prévus, pour ne perdre aucun produit.
    categorie_autre = None

    for produit in Produit.objects.all():
        categorie = correspondance.get(produit.categorie)
        if categorie is None:
            if categorie_autre is None:
                categorie_autre, _ = Categorie.objects.get_or_create(nom="Autre", defaults={"ordre": 99})
            categorie = categorie_autre
        produit.categorie_temp = categorie
        produit.save(update_fields=["categorie_temp"])


def revenir_en_arriere(apps, schema_editor):
    # Pas besoin de vraie logique de retour arrière pour ce projet.
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('produits', '0004_creer_categorie'),
    ]

    operations = [
        migrations.AddField(
            model_name='produit',
            name='categorie_temp',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='produits_temp',
                to='produits.categorie',
            ),
        ),
        migrations.RunPython(migrer_donnees_vers_categories, revenir_en_arriere),
    ]
