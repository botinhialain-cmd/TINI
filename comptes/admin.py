from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profil, PushToken


class ProfilInline(admin.StackedInline):
    model = Profil
    can_delete = False
    verbose_name_plural = "Profil (rôle)"


class UserAdminPersonnalise(UserAdmin):
    inlines = [ProfilInline]


admin.site.unregister(User)
admin.site.register(User, UserAdminPersonnalise)


@admin.register(PushToken)
class PushTokenAdmin(admin.ModelAdmin):
    list_display = ["user", "token", "date_creation"]
    ordering = ["-date_creation"]
