# API Reference

Base URL:

```text
http://127.0.0.1:8000/api
```

Protected endpoints require:

```text
Authorization: Bearer <access_token>
```

## Authentication

### Register

`POST /api/auth/register/`

Request:

```json
{
  "name": "Maya Patel",
  "email": "maya@example.com",
  "password": "StrongPass123!"
}
```

Response:

```json
{
  "message": "User registered successfully.",
  "user": {
    "id": 1,
    "name": "Maya Patel",
    "email": "maya@example.com",
    "date_joined": "2026-06-07T12:00:00Z"
  },
  "tokens": {
    "refresh": "...",
    "access": "..."
  }
}
```

### Login

`POST /api/auth/login/`

Request:

```json
{
  "email": "maya@example.com",
  "password": "StrongPass123!"
}
```

Response:

```json
{
  "refresh": "...",
  "access": "...",
  "user": {
    "id": 1,
    "name": "Maya Patel",
    "email": "maya@example.com",
    "date_joined": "2026-06-07T12:00:00Z"
  }
}
```

## Patients

### Create Patient

`POST /api/patients/`

```json
{
  "full_name": "Rahul Mehta",
  "date_of_birth": "1994-05-12",
  "gender": "male",
  "phone": "9876543210",
  "email": "rahul@example.com",
  "address": "Mumbai",
  "blood_group": "O+",
  "medical_history": "Hypertension",
  "allergies": "Penicillin",
  "emergency_contact": "Anita Mehta, 9876500000"
}
```

### List Patients

`GET /api/patients/`

Returns only patients created by the authenticated user.

### Patient Detail

`GET /api/patients/<id>/`

### Update Patient

`PUT /api/patients/<id>/`

Send the full patient object.

### Delete Patient

`DELETE /api/patients/<id>/`

## Doctors

### Create Doctor

`POST /api/doctors/`

```json
{
  "full_name": "Dr. Kavita Menon",
  "specialization": "Cardiology",
  "license_number": "MED-1001",
  "email": "kavita@example.com",
  "phone": "9988776655",
  "experience_years": 12,
  "clinic_address": "Care Clinic, Pune",
  "available": true
}
```

### List Doctors

`GET /api/doctors/`

Optional query params:

```text
?search=cardiology
?ordering=full_name
```

### Doctor Detail

`GET /api/doctors/<id>/`

### Update Doctor

`PUT /api/doctors/<id>/`

### Delete Doctor

`DELETE /api/doctors/<id>/`

## Patient-Doctor Mappings

### Assign Doctor to Patient

`POST /api/mappings/`

```json
{
  "patient": 1,
  "doctor": 2,
  "notes": "Cardiology referral"
}
```

Rules:

- The patient must belong to the authenticated user.
- The doctor must exist.
- The doctor must be available.
- The same doctor cannot be assigned to the same patient twice.

### List All Mappings

`GET /api/mappings/`

Returns mappings for patients owned by the authenticated user.

### List Doctors Assigned to One Patient

`GET /api/mappings/<patient_id>/`

Example:

```text
GET /api/mappings/1/
```

### Remove Mapping

`DELETE /api/mappings/<id>/`

Here `<id>` is the mapping id, not the patient id.

## Curl Examples

Register:

```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"Maya Patel\",\"email\":\"maya@example.com\",\"password\":\"StrongPass123!\"}"
```

Login:

```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"maya@example.com\",\"password\":\"StrongPass123!\"}"
```

Create patient:

```bash
curl -X POST http://127.0.0.1:8000/api/patients/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ACCESS_TOKEN_HERE" \
  -d "{\"full_name\":\"Rahul Mehta\",\"date_of_birth\":\"1994-05-12\",\"gender\":\"male\",\"blood_group\":\"O+\"}"
```

Create doctor:

```bash
curl -X POST http://127.0.0.1:8000/api/doctors/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ACCESS_TOKEN_HERE" \
  -d "{\"full_name\":\"Dr. Kavita Menon\",\"specialization\":\"Cardiology\",\"license_number\":\"MED-1001\",\"experience_years\":12,\"available\":true}"
```

Assign doctor:

```bash
curl -X POST http://127.0.0.1:8000/api/mappings/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ACCESS_TOKEN_HERE" \
  -d "{\"patient\":1,\"doctor\":1,\"notes\":\"Cardiology referral\"}"
```
