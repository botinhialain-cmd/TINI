from django.contrib import admin
from .models import Produit, Categorie


@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ["nom", "ordre", "actif"]
    list_editable = ["ordre", "actif"]
    ordering = ["ordre", "nom"]


@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ["nom", "format", "categorie", "prix", "cout", "disponible"]
    list_filter = ["categorie", "disponible"]
    list_editable = ["prix", "cout", "disponible"]
