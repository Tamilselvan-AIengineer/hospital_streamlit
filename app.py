import streamlit as st
import json
from datetime import date

# ---------- CONFIG ----------
st.set_page_config(page_title="NeoVitals Patient", layout="wide")

# ---------- JSON ----------
def load_data(file):
    try:
        with open(file, 'r') as f:
            return json.load(f)
    except:
        return []

def save_data(file, data):
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)

# ---------- SESSION ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = ""

# ---------- CSS ----------
st.markdown("""
<style>
.main {background-color:#f5f7fa;}
.sidebar .sidebar-content {background:#0e1117; color:white;}
.card {
    background:white;
    padding:20px;
    border-radius:12px;
    box-shadow:0px 4px 10px rgba(0,0,0,0.1);
}
.title {
    font-size:22px;
    font-weight:bold;
}
</style>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
st.sidebar.title("🏥 NeoVitals")

menu = ["Login", "Register"]

if st.session_state.logged_in:
    menu = ["Dashboard", "Book Appointment", "My Appointments", "My Profile", "Search"]

choice = st.sidebar.radio("Menu", menu)

# ---------- LOGIN ----------
if choice == "Login":
    st.title("🔐 Patient Login")

    username = st.text_input("Enter Name")
    if st.button("Login"):
        patients = load_data("patients.json")

        user = next((p for p in patients if p["name"] == username), None)

        if user:
            st.session_state.logged_in = True
            st.session_state.user = user
            st.success("Login Successful")
        else:
            st.error("Patient not found. Register first.")

# ---------- REGISTER ----------
elif choice == "Register":
    st.title("📝 Register as Patient")

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

        st.success("Registered Successfully. Now login.")

# ---------- DASHBOARD ----------
elif choice == "Dashboard":
    user = st.session_state.user
    st.title(f"👋 Welcome {user['name']}")

    appointments = load_data("appointments.json")
    my_appts = [a for a in appointments if a["patient_id"] == user["id"]]

    col1, col2, col3 = st.columns(3)

    col1.metric("My Appointments", len(my_appts))
    col2.metric("Age", user["age"])
    col3.metric("Status", "Active")

    st.markdown("### 📅 Upcoming Appointments")

    if my_appts:
        st.dataframe(my_appts)
    else:
        st.info("No appointments yet")

# ---------- BOOK ----------
elif choice == "Book Appointment":
    st.title("📅 Book Appointment")

    user = st.session_state.user

    doctor = st.selectbox("Select Doctor", ["Dr. Smith", "Dr. John", "Dr. Priya"])
    date_input = st.date_input("Choose Date", min_value=date.today())

    reason = st.text_area("Reason for Visit")

    if st.button("Confirm Booking"):
        appointments = load_data("appointments.json")

        appointment = {
            "patient_id": user["id"],
            "patient_name": user["name"],
            "doctor": doctor,
            "date": str(date_input),
            "reason": reason
        }

        appointments.append(appointment)
        save_data("appointments.json", appointments)

        st.success("Appointment Booked Successfully")

# ---------- MY APPOINTMENTS ----------
elif choice == "My Appointments":
    st.title("📋 My Appointments")

    user = st.session_state.user
    appointments = load_data("appointments.json")

    my_appts = [a for a in appointments if a["patient_id"] == user["id"]]

    if my_appts:
        st.dataframe(my_appts)

        cancel_id = st.number_input("Enter index to cancel", min_value=0)

        if st.button("Cancel Appointment"):
            try:
                del my_appts[cancel_id]
                save_data("appointments.json", appointments)
                st.success("Cancelled")
            except:
                st.error("Invalid selection")

    else:
        st.info("No appointments found")

# ---------- PROFILE ----------
elif choice == "My Profile":
    st.title("👤 My Profile")

    user = st.session_state.user

    st.write(user)

# ---------- SEARCH ----------
elif choice == "Search":
    st.title("🔍 Search Your Record")

    search = st.text_input("Search your name")

    patients = load_data("patients.json")

    result = [p for p in patients if search.lower() in p["name"].lower()]

    if search:
        if result:
            st.success("Record Found")
            st.dataframe(result)
        else:
            st.error("No record found")
