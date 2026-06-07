from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class AuthenticationTests(APITestCase):
    def test_user_can_register_and_login(self):
        register_response = self.client.post(
            reverse("register"),
            {
                "name": "Maya Patel",
                "email": "maya@example.com",
                "password": "StrongPass123!",
            },
            format="json",
        )

        self.assertEqual(register_response.status_code, status.HTTP_201_CREATED)
        self.assertIn("access", register_response.data["tokens"])

        login_response = self.client.post(
            reverse("login"),
            {
                "email": "maya@example.com",
                "password": "StrongPass123!",
            },
            format="json",
        )

        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIn("access", login_response.data)
        self.assertEqual(login_response.data["user"]["email"], "maya@example.com")
