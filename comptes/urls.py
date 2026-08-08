from django.urls import path
from .views import ConnexionView, EnregistrerPushTokenView

urlpatterns = [
    path("connexion/", ConnexionView.as_view(), name="connexion"),
    path("push-token/", EnregistrerPushTokenView.as_view(), name="push-token"),
]
