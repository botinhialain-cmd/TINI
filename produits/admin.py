from django.contrib import admin
from .models import Produit


@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ["nom", "format", "categorie", "prix", "disponible"]
    list_filter = ["categorie", "disponible"]
    list_editable = ["prix", "disponible"]
