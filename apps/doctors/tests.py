from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Doctor

User = get_user_model()


class DoctorAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            name="Aisha Rao",
            email="doctor-tests@example.com",
            password="StrongPass123!",
        )
        self.client.force_authenticate(self.user)

    def test_authenticated_user_can_create_and_list_doctors(self):
        response = self.client.post(
            reverse("doctor-list"),
            {
                "full_name": "Dr. Kavita Menon",
                "specialization": "Cardiology",
                "license_number": "med-1001",
                "email": "kavita@example.com",
                "phone": "9988776655",
                "experience_years": 12,
                "available": True,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Doctor.objects.get().license_number, "MED-1001")

        list_response = self.client.get(reverse("doctor-list"))
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(list_response.data), 1)

    def test_doctor_endpoints_require_authentication(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse("doctor-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
