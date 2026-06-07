from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.patients.models import Patient

from .models import PatientDoctorMapping
from .serializers import PatientDoctorMappingSerializer


class PatientDoctorMappingListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = PatientDoctorMappingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            PatientDoctorMapping.objects.select_related("patient", "doctor", "assigned_by")
            .filter(patient__owner=self.request.user)
        )

    def perform_create(self, serializer):
        serializer.save(assigned_by=self.request.user)


class PatientDoctorMappingDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PatientDoctorMapping.objects.select_related("patient", "doctor", "assigned_by").filter(
            patient__owner=self.request.user
        )

    def get(self, request, pk):
        patient = get_object_or_404(Patient, pk=pk, owner=request.user)
        mappings = self.get_queryset().filter(patient=patient)
        serializer = PatientDoctorMappingSerializer(mappings, many=True, context={"request": request})
        return Response(serializer.data)

    def delete(self, request, pk):
        mapping = get_object_or_404(self.get_queryset(), pk=pk)
        mapping.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
