from rest_framework import serializers

from apps.doctors.models import Doctor
from apps.patients.models import Patient

from .models import PatientDoctorMapping


class PatientDoctorMappingSerializer(serializers.ModelSerializer):
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.none())
    doctor = serializers.PrimaryKeyRelatedField(queryset=Doctor.objects.all())
    patient_name = serializers.CharField(source="patient.full_name", read_only=True)
    doctor_name = serializers.CharField(source="doctor.full_name", read_only=True)
    doctor_specialization = serializers.CharField(source="doctor.specialization", read_only=True)

    class Meta:
        model = PatientDoctorMapping
        fields = (
            "id",
            "patient",
            "patient_name",
            "doctor",
            "doctor_name",
            "doctor_specialization",
            "notes",
            "assigned_at",
        )
        read_only_fields = ("id", "patient_name", "doctor_name", "doctor_specialization", "assigned_at")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.user and request.user.is_authenticated:
            self.fields["patient"].queryset = Patient.objects.filter(owner=request.user)

    def validate(self, attrs):
        patient = attrs.get("patient")
        doctor = attrs.get("doctor")

        if doctor and not doctor.available:
            raise serializers.ValidationError({"doctor": "This doctor is currently marked unavailable."})

        if patient and doctor:
            duplicate = PatientDoctorMapping.objects.filter(patient=patient, doctor=doctor)
            if self.instance:
                duplicate = duplicate.exclude(pk=self.instance.pk)
            if duplicate.exists():
                raise serializers.ValidationError("This doctor is already assigned to the selected patient.")

        return attrs
