from django.urls import path

from .views import PatientDoctorMappingDetailAPIView, PatientDoctorMappingListCreateAPIView

urlpatterns = [
    path("", PatientDoctorMappingListCreateAPIView.as_view(), name="mapping-list"),
    path("<int:pk>/", PatientDoctorMappingDetailAPIView.as_view(), name="mapping-detail"),
]
