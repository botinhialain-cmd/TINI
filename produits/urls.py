from django.urls import path
from .views import ProduitListView

urlpatterns = [
    path("", ProduitListView.as_view(), name="produit-list"),
]
