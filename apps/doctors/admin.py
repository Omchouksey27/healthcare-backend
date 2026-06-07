from django.contrib import admin

from .models import Doctor


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ("full_name", "specialization", "license_number", "available", "created_at")
    list_filter = ("specialization", "available", "created_at")
    search_fields = ("full_name", "specialization", "license_number", "email", "phone")
    readonly_fields = ("created_at", "updated_at")
