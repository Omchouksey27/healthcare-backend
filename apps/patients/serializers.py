from django.utils import timezone
from rest_framework import serializers

from .models import Patient


class PatientSerializer(serializers.ModelSerializer):
    age = serializers.ReadOnlyField()

    class Meta:
        model = Patient
        fields = (
            "id",
            "full_name",
            "date_of_birth",
            "age",
            "gender",
            "phone",
            "email",
            "address",
            "blood_group",
            "medical_history",
            "allergies",
            "emergency_contact",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "age", "created_at", "updated_at")

    def validate_full_name(self, value):
        name = value.strip()
        if not name:
            raise serializers.ValidationError("Patient name is required.")
        return name

    def validate_date_of_birth(self, value):
        if value > timezone.localdate():
            raise serializers.ValidationError("Date of birth cannot be in the future.")
        return value
