from django.urls import path

from .views import PatientDetailAPIView, PatientListCreateAPIView

urlpatterns = [
    path("", PatientListCreateAPIView.as_view(), name="patient-list"),
    path("<int:pk>/", PatientDetailAPIView.as_view(), name="patient-detail"),
]
