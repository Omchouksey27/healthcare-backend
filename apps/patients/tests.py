from datetime import date

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Patient

User = get_user_model()


class PatientAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            name="Aisha Rao",
            email="aisha@example.com",
            password="StrongPass123!",
        )
        self.other_user = User.objects.create_user(
            name="Noah Smith",
            email="noah@example.com",
            password="StrongPass123!",
        )
        self.client.force_authenticate(self.user)

    def test_authenticated_user_can_create_and_list_own_patients(self):
        response = self.client.post(
            reverse("patient-list"),
            {
                "full_name": "Rahul Mehta",
                "date_of_birth": "1994-05-12",
                "gender": "male",
                "phone": "9876543210",
                "blood_group": "O+",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Patient.objects.count(), 1)

        list_response = self.client.get(reverse("patient-list"))
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(list_response.data), 1)

    def test_user_cannot_access_another_users_patient(self):
        other_patient = Patient.objects.create(
            owner=self.other_user,
            full_name="Private Patient",
            date_of_birth=date(1990, 1, 1),
            gender=Patient.Gender.OTHER,
        )

        response = self.client.get(reverse("patient-detail", args=[other_patient.id]))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
