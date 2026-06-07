from datetime import date

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.doctors.models import Doctor
from apps.patients.models import Patient

from .models import PatientDoctorMapping

User = get_user_model()


class PatientDoctorMappingAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            name="Aisha Rao",
            email="mapping-tests@example.com",
            password="StrongPass123!",
        )
        self.other_user = User.objects.create_user(
            name="Ishaan Roy",
            email="other-mapping@example.com",
            password="StrongPass123!",
        )
        self.patient = Patient.objects.create(
            owner=self.user,
            full_name="Nina Shah",
            date_of_birth=date(1988, 3, 20),
            gender=Patient.Gender.FEMALE,
        )
        self.other_patient = Patient.objects.create(
            owner=self.other_user,
            full_name="Hidden Patient",
            date_of_birth=date(1979, 8, 1),
            gender=Patient.Gender.OTHER,
        )
        self.doctor = Doctor.objects.create(
            created_by=self.user,
            full_name="Dr. Arjun Sen",
            specialization="Neurology",
            license_number="NEU-2001",
        )
        self.client.force_authenticate(self.user)

    def test_user_can_assign_doctor_to_own_patient(self):
        response = self.client.post(
            reverse("mapping-list"),
            {"patient": self.patient.id, "doctor": self.doctor.id, "notes": "Initial referral"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PatientDoctorMapping.objects.count(), 1)

    def test_user_cannot_assign_doctor_to_another_users_patient(self):
        response = self.client.post(
            reverse("mapping-list"),
            {"patient": self.other_patient.id, "doctor": self.doctor.id},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patient_mapping_list_uses_patient_id_for_get(self):
        PatientDoctorMapping.objects.create(patient=self.patient, doctor=self.doctor, assigned_by=self.user)

        response = self.client.get(reverse("mapping-detail", args=[self.patient.id]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
