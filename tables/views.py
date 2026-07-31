from rest_framework.generics import RetrieveAPIView
from .models import Table
from .serializers import TableSerializer


class TableParQRCodeView(RetrieveAPIView):
    """Récupère une table à partir du code_qr scanné par le client."""
    queryset = Table.objects.filter(active=True)
    serializer_class = TableSerializer
    lookup_field = "code_qr"
    lookup_url_kwarg = "code_qr"
