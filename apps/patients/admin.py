from django.contrib import admin

from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("full_name", "owner", "gender", "blood_group", "created_at")
    list_filter = ("gender", "blood_group", "created_at")
    search_fields = ("full_name", "email", "phone", "owner__email")
    readonly_fields = ("created_at", "updated_at")
