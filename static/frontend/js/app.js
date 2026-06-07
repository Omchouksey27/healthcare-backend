const API_BASE = document.body.dataset.apiBase || "/api";

const state = {
    access: localStorage.getItem("healthcare_access"),
    refresh: localStorage.getItem("healthcare_refresh"),
    user: JSON.parse(localStorage.getItem("healthcare_user") || "null"),
    patients: [],
    doctors: [],
    mappings: [],
};

const elements = {
    authSection: document.getElementById("authSection"),
    appSection: document.getElementById("appSection"),
    loginForm: document.getElementById("loginForm"),
    registerForm: document.getElementById("registerForm"),
    logoutBtn: document.getElementById("logoutBtn"),
    userChip: document.getElementById("userChip"),
    toast: document.getElementById("toast"),
    patientForm: document.getElementById("patientForm"),
    patientResetBtn: document.getElementById("patientResetBtn"),
    patientSubmitBtn: document.getElementById("patientSubmitBtn"),
    patientTableBody: document.getElementById("patientTableBody"),
    patientCount: document.getElementById("patientCount"),
    doctorForm: document.getElementById("doctorForm"),
    doctorResetBtn: document.getElementById("doctorResetBtn"),
    doctorSubmitBtn: document.getElementById("doctorSubmitBtn"),
    doctorTableBody: document.getElementById("doctorTableBody"),
    doctorCount: document.getElementById("doctorCount"),
    mappingForm: document.getElementById("mappingForm"),
    mappingPatientFilter: document.getElementById("mappingPatientFilter"),
    mappingResetBtn: document.getElementById("mappingResetBtn"),
    mappingTableBody: document.getElementById("mappingTableBody"),
    mappingCount: document.getElementById("mappingCount"),
};

function escapeHtml(value) {
    return String(value ?? "")
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}

function showToast(message, type = "success") {
    elements.toast.textContent = message;
    elements.toast.className = `toast ${type === "error" ? "error" : ""}`;
    window.clearTimeout(showToast.timeout);
    showToast.timeout = window.setTimeout(() => {
        elements.toast.classList.add("hidden");
    }, 4200);
}

function extractError(data) {
    if (!data) {
        return "Something went wrong.";
    }
    if (typeof data === "string") {
        return data;
    }
    if (data.detail) {
        return data.detail;
    }
    if (data.non_field_errors) {
        return data.non_field_errors.join(" ");
    }
    return Object.entries(data)
        .map(([key, value]) => `${key}: ${Array.isArray(value) ? value.join(" ") : value}`)
        .join(" ");
}

async function apiFetch(path, options = {}) {
    const headers = {
        "Content-Type": "application/json",
        ...(options.headers || {}),
    };

    if (state.access) {
        headers.Authorization = `Bearer ${state.access}`;
    }

    const response = await fetch(`${API_BASE}${path}`, {
        ...options,
        headers,
    });
    const text = await response.text();
    const data = text ? JSON.parse(text) : null;

    if (!response.ok) {
        if (response.status === 401) {
            clearSession();
            renderSession();
        }
        throw new Error(extractError(data));
    }

    return data;
}

function formDataToObject(form) {
    return Object.fromEntries(new FormData(form).entries());
}

function setSession(payload) {
    const tokens = payload.tokens || payload;
    state.access = tokens.access;
    state.refresh = tokens.refresh;
    state.user = payload.user || null;

    localStorage.setItem("healthcare_access", state.access);
    localStorage.setItem("healthcare_refresh", state.refresh);
    localStorage.setItem("healthcare_user", JSON.stringify(state.user));
}

function clearSession() {
    state.access = null;
    state.refresh = null;
    state.user = null;
    state.patients = [];
    state.doctors = [];
    state.mappings = [];
    localStorage.removeItem("healthcare_access");
    localStorage.removeItem("healthcare_refresh");
    localStorage.removeItem("healthcare_user");
}

function renderSession() {
    const signedIn = Boolean(state.access);
    elements.authSection.classList.toggle("hidden", signedIn);
    elements.appSection.classList.toggle("hidden", !signedIn);
    elements.logoutBtn.classList.toggle("hidden", !signedIn);
    elements.userChip.textContent = signedIn && state.user ? state.user.email : "Signed out";
}

function setActiveTab(name) {
    document.querySelectorAll(".tab-button").forEach((button) => {
        button.classList.toggle("active", button.dataset.tab === name);
    });
    document.querySelectorAll(".workspace-panel").forEach((panel) => {
        panel.classList.toggle("active", panel.dataset.panel === name);
    });
}

async function loadPatients() {
    state.patients = await apiFetch("/patients/");
    renderPatients();
    renderPatientOptions();
    renderMetrics();
}

async function loadDoctors() {
    state.doctors = await apiFetch("/doctors/");
    renderDoctors();
    renderDoctorOptions();
    renderMetrics();
}

async function loadMappings(patientId = "") {
    state.mappings = await apiFetch(patientId ? `/mappings/${patientId}/` : "/mappings/");
    renderMappings();
    renderMetrics();
}

async function bootstrapApp() {
    renderSession();
    if (!state.access) {
        return;
    }

    try {
        await Promise.all([loadPatients(), loadDoctors()]);
        await loadMappings();
    } catch (error) {
        showToast(error.message, "error");
    }
}

function renderMetrics() {
    elements.patientCount.textContent = state.patients.length;
    elements.doctorCount.textContent = state.doctors.length;
    elements.mappingCount.textContent = state.mappings.length;
}

function renderPatients() {
    if (!state.patients.length) {
        elements.patientTableBody.innerHTML = '<tr><td class="empty" colspan="6">No patients yet.</td></tr>';
        return;
    }

    elements.patientTableBody.innerHTML = state.patients
        .map(
            (patient) => `
            <tr>
                <td><strong>${escapeHtml(patient.full_name)}</strong></td>
                <td>${escapeHtml(patient.age)}</td>
                <td>${escapeHtml(patient.gender)}</td>
                <td>${escapeHtml(patient.blood_group)}</td>
                <td>${escapeHtml(patient.phone || patient.email || "-")}</td>
                <td>
                    <div class="row-actions">
                        <button class="table-button" type="button" data-action="patient-edit" data-id="${patient.id}">Edit</button>
                        <button class="table-button" type="button" data-action="patient-assignments" data-id="${patient.id}">Assignments</button>
                        <button class="danger-button table-button" type="button" data-action="patient-delete" data-id="${patient.id}">Delete</button>
                    </div>
                </td>
            </tr>
        `
        )
        .join("");
}

function renderDoctors() {
    if (!state.doctors.length) {
        elements.doctorTableBody.innerHTML = '<tr><td class="empty" colspan="6">No doctors yet.</td></tr>';
        return;
    }

    elements.doctorTableBody.innerHTML = state.doctors
        .map(
            (doctor) => `
            <tr>
                <td><strong>${escapeHtml(doctor.full_name)}</strong></td>
                <td>${escapeHtml(doctor.specialization)}</td>
                <td>${escapeHtml(doctor.license_number)}</td>
                <td>
                    <span class="status-pill ${doctor.available ? "ok" : "warn"}">
                        ${doctor.available ? "Available" : "Unavailable"}
                    </span>
                </td>
                <td>${escapeHtml(doctor.phone || doctor.email || "-")}</td>
                <td>
                    <div class="row-actions">
                        <button class="table-button" type="button" data-action="doctor-edit" data-id="${doctor.id}">Edit</button>
                        <button class="danger-button table-button" type="button" data-action="doctor-delete" data-id="${doctor.id}">Delete</button>
                    </div>
                </td>
            </tr>
        `
        )
        .join("");
}

function renderMappings() {
    if (!state.mappings.length) {
        elements.mappingTableBody.innerHTML = '<tr><td class="empty" colspan="6">No assignments yet.</td></tr>';
        return;
    }

    elements.mappingTableBody.innerHTML = state.mappings
        .map(
            (mapping) => `
            <tr>
                <td><strong>${escapeHtml(mapping.patient_name)}</strong></td>
                <td>${escapeHtml(mapping.doctor_name)}</td>
                <td>${escapeHtml(mapping.doctor_specialization)}</td>
                <td>${formatDate(mapping.assigned_at)}</td>
                <td>${escapeHtml(mapping.notes || "-")}</td>
                <td>
                    <button class="danger-button table-button" type="button" data-action="mapping-delete" data-id="${mapping.id}">
                        Remove
                    </button>
                </td>
            </tr>
        `
        )
        .join("");
}

function renderPatientOptions() {
    const options = state.patients
        .map((patient) => `<option value="${patient.id}">${escapeHtml(patient.full_name)}</option>`)
        .join("");
    elements.mappingForm.elements.patient.innerHTML = `<option value="">Select patient</option>${options}`;
    elements.mappingPatientFilter.innerHTML = `<option value="">All patients</option>${options}`;
}

function renderDoctorOptions() {
    const options = state.doctors
        .filter((doctor) => doctor.available)
        .map((doctor) => `<option value="${doctor.id}">${escapeHtml(doctor.full_name)} - ${escapeHtml(doctor.specialization)}</option>`)
        .join("");
    elements.mappingForm.elements.doctor.innerHTML = `<option value="">Select doctor</option>${options}`;
}

function formatDate(value) {
    if (!value) {
        return "-";
    }
    return new Intl.DateTimeFormat(undefined, { dateStyle: "medium" }).format(new Date(value));
}

function resetPatientForm() {
    elements.patientForm.reset();
    elements.patientForm.elements.id.value = "";
    elements.patientSubmitBtn.innerHTML = '<span aria-hidden="true">+</span> Save patient';
}

function resetDoctorForm() {
    elements.doctorForm.reset();
    elements.doctorForm.elements.id.value = "";
    elements.doctorForm.elements.available.checked = true;
    elements.doctorSubmitBtn.innerHTML = '<span aria-hidden="true">+</span> Save doctor';
}

function fillPatientForm(patient) {
    const fields = elements.patientForm.elements;
    fields.id.value = patient.id;
    fields.full_name.value = patient.full_name || "";
    fields.date_of_birth.value = patient.date_of_birth || "";
    fields.gender.value = patient.gender || "";
    fields.blood_group.value = patient.blood_group || "unknown";
    fields.phone.value = patient.phone || "";
    fields.email.value = patient.email || "";
    fields.address.value = patient.address || "";
    fields.medical_history.value = patient.medical_history || "";
    fields.allergies.value = patient.allergies || "";
    fields.emergency_contact.value = patient.emergency_contact || "";
    elements.patientSubmitBtn.innerHTML = '<span aria-hidden="true">OK</span> Update patient';
    window.scrollTo({ top: 0, behavior: "smooth" });
}

function fillDoctorForm(doctor) {
    const fields = elements.doctorForm.elements;
    fields.id.value = doctor.id;
    fields.full_name.value = doctor.full_name || "";
    fields.specialization.value = doctor.specialization || "";
    fields.license_number.value = doctor.license_number || "";
    fields.experience_years.value = doctor.experience_years ?? 0;
    fields.email.value = doctor.email || "";
    fields.phone.value = doctor.phone || "";
    fields.clinic_address.value = doctor.clinic_address || "";
    fields.available.checked = Boolean(doctor.available);
    elements.doctorSubmitBtn.innerHTML = '<span aria-hidden="true">OK</span> Update doctor';
    window.scrollTo({ top: 0, behavior: "smooth" });
}

async function deletePatient(id) {
    const patient = state.patients.find((item) => item.id === Number(id));
    if (!window.confirm(`Delete patient "${patient?.full_name || id}"?`)) {
        return;
    }
    await apiFetch(`/patients/${id}/`, { method: "DELETE" });
    await loadPatients();
    await loadMappings();
    showToast("Patient deleted.");
}

async function deleteDoctor(id) {
    const doctor = state.doctors.find((item) => item.id === Number(id));
    if (!window.confirm(`Delete doctor "${doctor?.full_name || id}"?`)) {
        return;
    }
    await apiFetch(`/doctors/${id}/`, { method: "DELETE" });
    await loadDoctors();
    await loadMappings();
    showToast("Doctor deleted.");
}

async function deleteMapping(id) {
    if (!window.confirm("Remove this assignment?")) {
        return;
    }
    await apiFetch(`/mappings/${id}/`, { method: "DELETE" });
    await loadMappings(elements.mappingPatientFilter.value);
    showToast("Assignment removed.");
}

function wireEvents() {
    document.querySelectorAll(".tab-button").forEach((button) => {
        button.addEventListener("click", () => setActiveTab(button.dataset.tab));
    });

    elements.loginForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        try {
            const payload = formDataToObject(elements.loginForm);
            const data = await apiFetch("/auth/login/", {
                method: "POST",
                body: JSON.stringify(payload),
            });
            setSession(data);
            elements.loginForm.reset();
            await bootstrapApp();
            showToast("Logged in successfully.");
        } catch (error) {
            showToast(error.message, "error");
        }
    });

    elements.registerForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        try {
            const payload = formDataToObject(elements.registerForm);
            const data = await apiFetch("/auth/register/", {
                method: "POST",
                body: JSON.stringify(payload),
            });
            setSession(data);
            elements.registerForm.reset();
            await bootstrapApp();
            showToast("Account created.");
        } catch (error) {
            showToast(error.message, "error");
        }
    });

    elements.logoutBtn.addEventListener("click", () => {
        clearSession();
        renderSession();
        showToast("Logged out.");
    });

    elements.patientResetBtn.addEventListener("click", resetPatientForm);
    elements.doctorResetBtn.addEventListener("click", resetDoctorForm);

    elements.patientForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        try {
            const payload = formDataToObject(elements.patientForm);
            const id = payload.id;
            delete payload.id;
            const method = id ? "PUT" : "POST";
            const path = id ? `/patients/${id}/` : "/patients/";
            await apiFetch(path, { method, body: JSON.stringify(payload) });
            resetPatientForm();
            await loadPatients();
            await loadMappings(elements.mappingPatientFilter.value);
            showToast(id ? "Patient updated." : "Patient created.");
        } catch (error) {
            showToast(error.message, "error");
        }
    });

    elements.doctorForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        try {
            const payload = formDataToObject(elements.doctorForm);
            const id = payload.id;
            delete payload.id;
            payload.available = elements.doctorForm.elements.available.checked;
            payload.experience_years = Number(payload.experience_years || 0);
            const method = id ? "PUT" : "POST";
            const path = id ? `/doctors/${id}/` : "/doctors/";
            await apiFetch(path, { method, body: JSON.stringify(payload) });
            resetDoctorForm();
            await loadDoctors();
            await loadMappings(elements.mappingPatientFilter.value);
            showToast(id ? "Doctor updated." : "Doctor created.");
        } catch (error) {
            showToast(error.message, "error");
        }
    });

    elements.mappingForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        try {
            const payload = formDataToObject(elements.mappingForm);
            payload.patient = Number(payload.patient);
            payload.doctor = Number(payload.doctor);
            await apiFetch("/mappings/", { method: "POST", body: JSON.stringify(payload) });
            elements.mappingForm.reset();
            await loadMappings(elements.mappingPatientFilter.value);
            showToast("Doctor assigned.");
        } catch (error) {
            showToast(error.message, "error");
        }
    });

    elements.mappingPatientFilter.addEventListener("change", async () => {
        try {
            await loadMappings(elements.mappingPatientFilter.value);
        } catch (error) {
            showToast(error.message, "error");
        }
    });

    elements.mappingResetBtn.addEventListener("click", async () => {
        elements.mappingPatientFilter.value = "";
        await loadMappings();
    });

    document.addEventListener("click", async (event) => {
        const actionButton = event.target.closest("[data-action]");
        if (!actionButton) {
            return;
        }

        const id = Number(actionButton.dataset.id);
        const action = actionButton.dataset.action;

        try {
            if (action === "patient-edit") {
                const patient = state.patients.find((item) => item.id === id);
                if (patient) {
                    fillPatientForm(patient);
                    setActiveTab("patients");
                }
            }
            if (action === "patient-delete") {
                await deletePatient(id);
            }
            if (action === "patient-assignments") {
                elements.mappingPatientFilter.value = String(id);
                await loadMappings(id);
                setActiveTab("mappings");
            }
            if (action === "doctor-edit") {
                const doctor = state.doctors.find((item) => item.id === id);
                if (doctor) {
                    fillDoctorForm(doctor);
                    setActiveTab("doctors");
                }
            }
            if (action === "doctor-delete") {
                await deleteDoctor(id);
            }
            if (action === "mapping-delete") {
                await deleteMapping(id);
            }
        } catch (error) {
            showToast(error.message, "error");
        }
    });
}

wireEvents();
bootstrapApp();
