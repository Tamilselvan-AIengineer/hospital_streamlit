import streamlit as st
import json
from datetime import date

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="NeoVitals HMS", layout="wide")

# ---------- LOAD / SAVE ----------
def load_data(file):
    try:
        with open(file, 'r') as f:
            return json.load(f)
    except:
        return []

def save_data(file, data):
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
body {background-color: #f5f7fa;}
.sidebar .sidebar-content {background-color: #0e1117;}
h1, h2, h3 {color: #0e1117;}
.card {
    background: white;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.1);
}
.metric {
    text-align: center;
    padding: 10px;
    border-radius: 10px;
    background: #e3f2fd;
}
</style>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
st.sidebar.title("🏥 NeoVitals")
menu = st.sidebar.radio("Navigation", [
    "Login",
    "Register",
    "Dashboard",
    "Book Appointment",
    "View Appointments",
    "Search Patient"
])

# ---------- LOGIN ----------
if menu == "Login":
    st.title("🔐 Login")

    col1, col2 = st.columns([1,1])

    with col1:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if username == "admin" and password == "123":
                st.success("Login Successful")
            else:
                st.error("Invalid Credentials")

# ---------- PATIENT REGISTRATION ----------
elif menu == "Register":
    st.title("📝 Patient Registration")

    with st.form("register_form"):
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Name")
            age = st.number_input("Age", min_value=0)
        with col2:
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            phone = st.text_input("Phone")

        submit = st.form_submit_button("Register")

        if submit:
            if not name:
                st.error("Name is required")
            else:
                patients = load_data("patients.json")

                patient = {
                    "id": len(patients) + 1,
                    "name": name,
                    "age": age,
                    "gender": gender,
                    "phone": phone
                }

                patients.append(patient)
                save_data("patients.json", patients)

                st.success(f"Patient Registered (ID: {patient['id']})")

# ---------- DASHBOARD ----------
elif menu == "Dashboard":
    st.title("📊 Patient Dashboard")

    patients = load_data("patients.json")
    appointments = load_data("appointments.json")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Patients", len(patients))
    col2.metric("Appointments", len(appointments))
    col3.metric("System Status", "Active")

    st.markdown("### 👤 Patient List")
    st.dataframe(patients)

# ---------- BOOK APPOINTMENT ----------
elif menu == "Book Appointment":
    st.title("📅 Book Appointment")

    patients = load_data("patients.json")

    if len(patients) == 0:
        st.warning("No patients available. Register first.")
    else:
        patient_names = [p["name"] for p in patients]
        selected_patient = st.selectbox("Select Patient", patient_names)

        doctor = st.text_input("Doctor Name")
        appointment_date = st.date_input("Date", min_value=date.today())

        if st.button("Book"):
            patient_id = next(p["id"] for p in patients if p["name"] == selected_patient)

            appointments = load_data("appointments.json")

            appointment = {
                "patient_id": patient_id,
                "patient_name": selected_patient,
                "doctor": doctor,
                "date": str(appointment_date)
            }

            appointments.append(appointment)
            save_data("appointments.json", appointments)

            st.success("Appointment Booked")

# ---------- VIEW APPOINTMENTS ----------
elif menu == "View Appointments":
    st.title("📋 Appointments")

    appointments = load_data("appointments.json")

    if len(appointments) == 0:
        st.info("No appointments found")
    else:
        st.dataframe(appointments)

# ---------- SEARCH PATIENT ----------
elif menu == "Search Patient":
    st.title("🔍 Search Patient")

    search = st.text_input("Enter Patient Name")

    patients = load_data("patients.json")

    results = [p for p in patients if search.lower() in p["name"].lower()]

    if search:
        if results:
            st.success("Patient Found")
            st.dataframe(results)
        else:
            st.error("No patient found")
