import streamlit as st
import json
from datetime import date

# ---------- CONFIG ----------
st.set_page_config(page_title="NeoVitals", layout="wide")

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
    st.session_state.user = None

# ---------- PREMIUM CSS ----------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #eef2f7, #e3f2fd);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #0e1117;
    color: white;
}

/* Cards */
.card {
    background: rgba(255,255,255,0.8);
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 6px 15px rgba(0,0,0,0.1);
    margin-bottom: 15px;
}

/* Title */
.title {
    font-size: 28px;
    font-weight: bold;
}

/* Metric box */
.metric-box {
    background: white;
    padding: 15px;
    border-radius: 12px;
    text-align: center;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
}

/* Appointment card */
.appt {
    background: #ffffff;
    padding: 15px;
    border-left: 5px solid #4CAF50;
    border-radius: 10px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
st.sidebar.title("🏥 NeoVitals")

menu = ["Login", "Register"]

if st.session_state.logged_in:
    menu = ["Dashboard", "Book Appointment", "My Appointments", "My Profile", "Search"]

choice = st.sidebar.radio("Navigation", menu)

# ---------- LOGIN ----------
if choice == "Login":
    st.markdown("<div class='title'>🔐 Patient Login</div>", unsafe_allow_html=True)

    name = st.text_input("Enter your name")

    if st.button("Login"):
        patients = load_data("patients.json")
        user = next((p for p in patients if p["name"] == name), None)

        if user:
            st.session_state.logged_in = True
            st.session_state.user = user
            st.success("Login Successful")
        else:
            st.error("Patient not found")

# ---------- REGISTER ----------
elif choice == "Register":
    st.markdown("<div class='title'>📝 Register</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=0)

    with col2:
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

        st.success("Registered Successfully")

# ---------- DASHBOARD ----------
elif choice == "Dashboard":
    user = st.session_state.user
    st.markdown(f"<div class='title'>👋 Welcome, {user['name']}</div>", unsafe_allow_html=True)

    appointments = load_data("appointments.json")
    my_appts = [a for a in appointments if a["patient_id"] == user["id"]]

    # Metrics
    col1, col2, col3 = st.columns(3)

    col1.markdown(f"<div class='metric-box'><h3>{len(my_appts)}</h3>Appointments</div>", unsafe_allow_html=True)
    col2.markdown(f"<div class='metric-box'><h3>{user['age']}</h3>Age</div>", unsafe_allow_html=True)
    col3.markdown(f"<div class='metric-box'><h3>Active</h3>Status</div>", unsafe_allow_html=True)

    st.markdown("### 📅 Upcoming Appointments")

    for a in my_appts:
        st.markdown(f"""
        <div class='appt'>
            <b>Doctor:</b> {a['doctor']}<br>
            <b>Date:</b> {a['date']}<br>
            <b>Reason:</b> {a['reason']}
        </div>
        """, unsafe_allow_html=True)

# ---------- BOOK ----------
elif choice == "Book Appointment":
    st.markdown("<div class='title'>📅 Book Appointment</div>", unsafe_allow_html=True)

    user = st.session_state.user

    col1, col2 = st.columns(2)

    with col1:
        doctor = st.selectbox("Doctor", ["Dr. Priya", "Dr. Arun", "Dr. John"])
        date_input = st.date_input("Date", min_value=date.today())

    with col2:
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

        st.success("Appointment Booked")

# ---------- MY APPOINTMENTS ----------
elif choice == "My Appointments":
    st.markdown("<div class='title'>📋 My Appointments</div>", unsafe_allow_html=True)

    user = st.session_state.user
    appointments = load_data("appointments.json")

    my_appts = [a for a in appointments if a["patient_id"] == user["id"]]

    for i, a in enumerate(my_appts):
        st.markdown(f"""
        <div class='appt'>
            <b>{i}</b> | {a['doctor']} | {a['date']}
        </div>
        """, unsafe_allow_html=True)

    cancel_index = st.number_input("Enter index to cancel", min_value=0)

    if st.button("Cancel"):
        if cancel_index < len(my_appts):
            del appointments[cancel_index]
            save_data("appointments.json", appointments)
            st.success("Cancelled")

# ---------- PROFILE ----------
elif choice == "My Profile":
    user = st.session_state.user
    st.markdown("<div class='title'>👤 My Profile</div>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class='card'>
        <b>Name:</b> {user['name']}<br>
        <b>Age:</b> {user['age']}<br>
        <b>Gender:</b> {user['gender']}<br>
        <b>Phone:</b> {user['phone']}
    </div>
    """, unsafe_allow_html=True)

# ---------- SEARCH ----------
elif choice == "Search":
    st.markdown("<div class='title'>🔍 Search</div>", unsafe_allow_html=True)

    search = st.text_input("Search name")

    patients = load_data("patients.json")

    results = [p for p in patients if search.lower() in p["name"].lower()]

    for r in results:
        st.markdown(f"""
        <div class='card'>
            <b>{r['name']}</b><br>
            Age: {r['age']}<br>
            Phone: {r['phone']}
        </div>
        """, unsafe_allow_html=True)
