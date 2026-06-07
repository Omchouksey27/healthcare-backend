from django.conf import settings
from django.db import models


class PatientDoctorMapping(models.Model):
    patient = models.ForeignKey("patients.Patient", related_name="doctor_mappings", on_delete=models.CASCADE)
    doctor = models.ForeignKey("doctors.Doctor", related_name="patient_mappings", on_delete=models.CASCADE)
    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="doctor_assignments",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    notes = models.TextField(blank=True)
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-assigned_at",)
        constraints = [
            models.UniqueConstraint(fields=["patient", "doctor"], name="unique_patient_doctor_assignment"),
        ]
        indexes = [
            models.Index(fields=["patient", "assigned_at"]),
        ]

    def __str__(self):
        return f"{self.patient} assigned to {self.doctor}"
