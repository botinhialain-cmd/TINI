from django.urls import path
from .views import TableParQRCodeView

urlpatterns = [
    path("<uuid:code_qr>/", TableParQRCodeView.as_view(), name="table-detail"),
]
