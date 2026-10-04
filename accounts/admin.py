from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    ordering = ("email",)
    list_display = ("email", "full_name", "is_staff", "date_joined")
    fieldsets = ((None, {"fields": ("email", "password")}), ("Dados", {"fields": ("full_name", "accepted_terms", "consented_at")}), ("Permissões", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}), ("Datas", {"fields": ("last_login", "date_joined")}))
    add_fieldsets = ((None, {"classes": ("wide",), "fields": ("email", "full_name", "password1", "password2")}),)
    search_fields = ("email", "full_name")
