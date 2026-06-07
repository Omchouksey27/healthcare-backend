from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Doctor",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("full_name", models.CharField(max_length=150)),
                ("specialization", models.CharField(max_length=120)),
                ("license_number", models.CharField(max_length=80, unique=True)),
                ("email", models.EmailField(blank=True, max_length=254)),
                ("phone", models.CharField(blank=True, max_length=25)),
                ("experience_years", models.PositiveSmallIntegerField(default=0)),
                ("clinic_address", models.TextField(blank=True)),
                ("available", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="created_doctors",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ("full_name",),
            },
        ),
        migrations.AddIndex(
            model_name="doctor",
            index=models.Index(fields=["specialization"], name="doctors_doc_special_037046_idx"),
        ),
        migrations.AddIndex(
            model_name="doctor",
            index=models.Index(fields=["available"], name="doctors_doc_availab_0b6f10_idx"),
        ),
    ]
