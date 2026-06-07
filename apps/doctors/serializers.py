from rest_framework import serializers

from .models import Doctor


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = (
            "id",
            "full_name",
            "specialization",
            "license_number",
            "email",
            "phone",
            "experience_years",
            "clinic_address",
            "available",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")

    def validate_full_name(self, value):
        name = value.strip()
        if not name:
            raise serializers.ValidationError("Doctor name is required.")
        return name

    def validate_specialization(self, value):
        specialization = value.strip()
        if not specialization:
            raise serializers.ValidationError("Specialization is required.")
        return specialization

    def validate_license_number(self, value):
        license_number = value.strip().upper()
        if not license_number:
            raise serializers.ValidationError("License number is required.")
        duplicate = Doctor.objects.filter(license_number=license_number)
        if self.instance:
            duplicate = duplicate.exclude(pk=self.instance.pk)
        if duplicate.exists():
            raise serializers.ValidationError("A doctor with this license number already exists.")
        return license_number

    def validate_experience_years(self, value):
        if value > 80:
            raise serializers.ValidationError("Experience years looks too high.")
        return value
