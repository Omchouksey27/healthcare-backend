from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("doctors", "0001_initial"),
        ("patients", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="PatientDoctorMapping",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("notes", models.TextField(blank=True)),
                ("assigned_at", models.DateTimeField(auto_now_add=True)),
                (
                    "assigned_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="doctor_assignments",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "doctor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="patient_mappings",
                        to="doctors.doctor",
                    ),
                ),
                (
                    "patient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="doctor_mappings",
                        to="patients.patient",
                    ),
                ),
            ],
            options={
                "ordering": ("-assigned_at",),
            },
        ),
        migrations.AddIndex(
            model_name="patientdoctormapping",
            index=models.Index(fields=["patient", "assigned_at"], name="mappings_pa_patient_932fd0_idx"),
        ),
        migrations.AddConstraint(
            model_name="patientdoctormapping",
            constraint=models.UniqueConstraint(fields=("patient", "doctor"), name="unique_patient_doctor_assignment"),
        ),
    ]
