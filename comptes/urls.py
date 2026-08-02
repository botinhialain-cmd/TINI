from django.urls import path
from .views import ConnexionView

urlpatterns = [
    path("connexion/", ConnexionView.as_view(), name="connexion"),
]
