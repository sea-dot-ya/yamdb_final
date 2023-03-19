from django.contrib import admin

# Register your models here.
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "password",
        "last_login",
        "first_name",
        "last_name",
        "email",
        "is_staff",
        "is_active",
        "date_joined",
        "bio",
        "role",
        "is_superuser"
    )
    search_fields = ("username",)
    empty_value_display = "-пусто-"
    readonly_fields = ("is_superuser",)


admin.site.register(User, UserAdmin)
