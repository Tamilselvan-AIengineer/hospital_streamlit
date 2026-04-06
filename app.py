import streamlit as st
import json
from datetime import date

# ---------- Load JSON ----------
def load_data(file):
    try:
        with open(file, 'r') as f:
            return json.load(f)
    except:
        return []

def save_data(file, data):
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)

# ---------- UI ----------
st.title("🏥 Hospital Management System")

menu = ["Login", "Patient Registration", "Appointment Booking"]
choice = st.sidebar.selectbox("Menu", menu)

# ---------- Login ----------
if choice == "Login":
    st.subheader("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type='password')

    if st.button("Login"):
        if username == "admin" and password == "123":
            st.success("Login Successful")
        else:
            st.error("Invalid Credentials")

# ---------- Patient Registration ----------
elif choice == "Patient Registration":
    st.subheader("Register Patient")

    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    phone = st.text_input("Phone")

    if st.button("Register"):
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

        st.success(f"Patient Registered with ID {patient['id']}")

# ---------- Appointment ----------
elif choice == "Appointment Booking":
    st.subheader("Book Appointment")

    patient_id = st.number_input("Patient ID", min_value=1)
    doctor = st.text_input("Doctor Name")
    appointment_date = st.date_input("Date", min_value=date.today())

    if st.button("Book Appointment"):
        appointments = load_data("appointments.json")

        appointment = {
            "patient_id": patient_id,
            "doctor": doctor,
            "date": str(appointment_date)
        }

        appointments.append(appointment)
        save_data("appointments.json", appointments)

        st.success("Appointment Booked Successfully")
