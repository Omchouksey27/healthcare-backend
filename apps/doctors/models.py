from django.conf import settings
from django.db import models


class Doctor(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="created_doctors",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    full_name = models.CharField(max_length=150)
    specialization = models.CharField(max_length=120)
    license_number = models.CharField(max_length=80, unique=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=25, blank=True)
    experience_years = models.PositiveSmallIntegerField(default=0)
    clinic_address = models.TextField(blank=True)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("full_name",)
        indexes = [
            models.Index(fields=["specialization"]),
            models.Index(fields=["available"]),
        ]

    def __str__(self):
        return f"{self.full_name} - {self.specialization}"
