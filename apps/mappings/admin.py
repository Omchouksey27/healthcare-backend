from django.contrib import admin

from .models import PatientDoctorMapping


@admin.register(PatientDoctorMapping)
class PatientDoctorMappingAdmin(admin.ModelAdmin):
    list_display = ("patient", "doctor", "assigned_by", "assigned_at")
    list_filter = ("assigned_at", "doctor__specialization")
    search_fields = ("patient__full_name", "doctor__full_name", "doctor__specialization")
    readonly_fields = ("assigned_at",)
