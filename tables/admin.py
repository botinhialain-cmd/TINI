from django.contrib import admin
from .models import Table


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ["numero", "code_qr", "active", "date_creation"]
    readonly_fields = ["code_qr"]
