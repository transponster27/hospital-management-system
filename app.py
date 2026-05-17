import streamlit as st
import requests
import pandas as pd
from datetime import date

BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Hospital Management System",
    layout="wide"
)
st.title("Hospital Management System")

menu = st.sidebar.selectbox(
    "Choose Module",
    [
        "Home",
        "Patients",
        "Doctors",
        "Appointments",
        "Treatments",
        "Billing",
        "Patient History",
        "Doctor Workload"
    ]
)

if menu == "Home":
    st.header("Hospital Dashboard")
    st.info("Use the sidebar to manage hospital records.")

elif menu == "Patients":

    action = st.selectbox(
        "Patient Actions",
        [
            "Add Patient",
            "Search Patient",
            "Update Patient",
            "Delete Patient",
            "Show All Patients"
        ]
    )
    if action == "Add Patient":
        st.subheader("Add New Patient")
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First Name")
            gender = st.selectbox("Gender", ["M", "F"])
            contact_number = st.text_input("Contact Number")
            insurance_provider = st.text_input("Insurance Provider")
            registration_date = st.date_input("Registration Date", value=date.today())
        with col2:
            last_name = st.text_input("Last Name")
            date_of_birth = st.date_input("Date of Birth", value=date(2000,1,1), min_value=date(1900,1,1), max_value=date.today())
            address = st.text_input("Address")
            insurance_number = st.text_input("Insurance Number")
            email = st.text_input("Email")
    
        if st.button("Create Patient"):
            params = {
                "first_name": first_name,
                "last_name": last_name,
                "gender": gender,
                "date_of_birth": str(date_of_birth),
                "contact_number": contact_number,
                "address": address,
                "registration_date": str(registration_date),
                "insurance_provider": insurance_provider,
                "insurance_number": insurance_number,
                "email": email
            }
            response = requests.post(f"{BASE_URL}/patients", params=params)
            if response.status_code == 200:
                st.success("Patient created successfully")
                st.json(response.json())
            else:
                st.error(response.json())

    elif action == "Search Patient":
        st.subheader("Search Patient")
        patient_id = st.text_input("Patient ID")
        first_name = st.text_input("First Name")
        if st.button("Search"):
            params = {}
            if patient_id:
                params["patient_id"] = patient_id
            if first_name:
                params["first_name"] = first_name
            response = requests.get(f"{BASE_URL}/patients", params=params)
            if response.status_code == 200:
                data = response.json()["data"]
                df = pd.DataFrame(data)
                st.dataframe(df, use_container_width=True)
            else:
                st.error(response.json())

    elif action == "Update Patient":
        st.subheader("Update Patient")
        patient_id = st.text_input("Patient ID")
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        email = st.text_input("Email")
        if st.button("Update"):
            params = {"patient_id": patient_id, "first_name": first_name, "last_name": last_name, "email": email }
            response = requests.put(f"{BASE_URL}/patients", params=params)
            if response.status_code==200:
                st.success("Patient updated")
                st.json(response.json())
            else:
                st.error(response.json())

    elif action=="Delete Patient":
        st.subheader("Delete Patient")
        patient_id=st.text_input("Patient ID")
        if st.button("Delete"):
            response=requests.delete(f"{BASE_URL}/patients?patient_id={patient_id}")
            if response.status_code==200:
                st.success("Patient deleted")
                st.json(response.json())
            else:
                st.error(response.json())
    
    elif action=="Show all Patients":
        response = requests.get(f"{BASE_URL}/patients/show all records")
        if response.status_code==200:
            df=pd.DataFrame(response.json()["data"])
            print(df)
            st.dataframe(df, use_container_width=True)
        else:
            st.error(response.json())

elif menu == "Doctors":
    st.header("Doctor Records")
    doctor_id = st.text_input("Doctor ID")
    first_name = st.text_input("Doctor First Name")
    specialization = st.text_input("Specialization")
    phone_number = st.text_input("Phone Number")
    years_experience = st.text_input("Years of Experience")
    hospital_branch = st.text_input("Hospital Branch")
    email = st.text_input("Email")
    if st.button("Search Doctor"):
        params = {}
        if doctor_id:
            params["doctor_id"] = doctor_id
        if first_name:
            params["first_name"] = first_name
        if specialization:
            params["specialization"] = specialization
        response = requests.get(f"{BASE_URL}/doctors", params=params)
        if response.status_code == 200:
            data = response.json()["data"]
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True)
        else:
            st.error(response.json())
    elif st.button("Update Doctor"):
        params = {
            "doctor_id": doctor_id,
            "first_name": first_name,
            "last_name": last_name,
            "specialization": specialization,
            "phone_number": phone_number,
            "years_experience": years_experience,
            "hospital_branch": hospital_branch,
            "email": email
        }
        response = requests.put(f"{BASE_URL}/doctors", params=params)
        if response.status_code == 200:
            st.success("Doctor updated successfully")
            st.json(response.json())
        else:
            st.error(response.json())        

elif menu == "Appointments":
    action = st.selectbox(
        "Appointment Actions",
        [
            "Create Appointment",
            "Search Appointment",
            "Update Appointment"
        ]
    )
    if action == "Create Appointment":
        st.subheader("Create Appointment")
        patient_id = st.text_input("Patient ID")
        doctor_id = st.text_input("Doctor ID")
        appointment_date = st.date_input("Appointment Date", min_value=date.today())
        appointment_time = st.time_input("Appointment Time")
        reason_for_visit = st.text_input("Reason for Visit")
        if st.button("Create"):
            params = {
                "patient_id": patient_id,
                "doctor_id": doctor_id,
                "appointment_date": str(appointment_date),
                "appointment_time": str(appointment_time),
                "reason_for_visit": reason_for_visit
            }
            response = requests.post(f"{BASE_URL}/appointments", params=params)
            if response.status_code == 200:
                st.success("Appointment created successfully")
                st.json(response.json())
            else:
                st.error(response.json())
    
    if action == "Search Appointment":
        st.subheader("Search Appointment")
        appointment_id = st.text_input("Appointment ID")
        first_name = st.text_input("Patient First Name")
        if st.button("Search"):
            params = { 
                "appointment_id": appointment_id,
                "first_name": first_name
            }
            response = requests.get(f"{BASE_URL}/appointments", params=params)
            if response.status_code == 200:
                df = pd.DataFrame(response.json()["data"])
                st.dataframe(df, use_container_width=True)
            else:
                st.error(response.json())
    
    if action == "Update Appointment":
        st.subheader("Update Appointment")
        appointment_id = st.text_input("Appointment ID")
        status = st.selectbox("Status", ["Scheduled", "Completed", "Cancelled"])
        appointment_date = st.date_input("Appointment Date")
        appointment_time = st.text_input("Appointment Time")
        if st.button("Update"):
            params = {
                "appointment_id": appointment_id,
                "status": status,
                "appointment_date": str(appointment_date),
                "appointment_time": appointment_time
            }
            response = requests.put(f"{BASE_URL}/appointments", params=params)
            if response.status_code == 200:
                st.success("Appointment updated successfully")
                st.json(response.json())
            else:
                st.error(response.json())

elif menu == "Treatments":
    action = st.selectbox(
        "Treatment Actions",
        [
            "Create Treatment",
            "Search Treatment",
            "Update Treatment"
        ]
    )
    if action == "Create Treatment":
        st.subheader("Create Treatment")
        appointment_id = st.text_input("Appointment ID")
        treatment_type = st.text_input("Treatment Type")
        description = st.text_input("Description")
        cost = st.number_input("Cost")
        treatment_date = st.date_input("Treatment Date", min_value=date.today())
        if st.button("Create"):
            params = {
                "appointment_id": appointment_id,
                "treatment_type": treatment_type,
                "description": description,
                "cost": cost,
                "treatment_date": str(treatment_date)
            }
            response = requests.post(f"{BASE_URL}/treatments", params=params)
            if response.status_code == 200:
                st.success("Treatment created successfully")
                st.json(response.json())
            else:
                st.error(response.json())

    if action == "Search Treatment":
        st.subheader("Search Treatment")
        treatment_id = st.text_input("Treatment ID")
        treatment_type = st.text_input("Treatment Type")
        if st.button("Search"):
            params = {
                "treatment_id": treatment_id,
                "treatment_type": treatment_type
            }
            response = requests.get(f"{BASE_URL}/treatment", params=params)
            if response.status_code == 200:
                df = pd.DataFrame(response.json()["data"])
                st.dataframe(df, use_container_width=True)
            else:
                st.error(response.json())

    if action == "Update Treatment":
        st.subheader("Update Treatment")
        treatment_id = st.text_input("Treatment ID")
        if st.button("Update"):
            params = {
                "treatment_id": treatment_id
            }
            response = requests.put(f"{BASE_URL}/treatments", params=params)
            if response.status_code == 200:
                st.success("Treatment updated successfully")
                st.json(response.json())
            else:
                st.error(response.json())

elif menu == "Billing":
    action = st.selectbox(
        "Billing Actions",
        [
            "Search Billing",
            "Update Billing"
        ]
    )
    if action == "Search Billing":
        st.subheader("Search Billing")
        bill_id = st.text_input("Bill ID")
        patient_id = st.text_input("Patient ID")
        if st.button("Search"):
            params = {
                    "bill_id": bill_id,
                    "patient_id": patient_id
                }
            response = requests.get(f"{BASE_URL}/billing", params=params)
            if response.status_code == 200:
                df = pd.DataFrame(response.json()["data"])
                st.dataframe(df, use_container_width=True)
            else:
                st.error(response.json())

    if action == "Update Billing":
        st.subheader("Update Billing")
        bill_id = st.text_input("Bill ID")
        patient_id = st.text_input("Patient ID")
        if st.button("Update"):
            params = {
                "bill_id": bill_id,
                "patient_id": patient_id
            }            
            response = requests.put(f"{BASE_URL}/billing", params=params)
            if response.status_code == 200:
                st.success("Billing updated successfully")
                st.json(response.json())
            else:
                st.error(response.json())

elif menu == "Patient History":
    st.header("View Patient History")
    patient_id = st.text_input("Patient ID")
    if st.button("Search"):
        params = {
            "patient_id": patient_id
        }
        response = requests.get(f"{BASE_URL}/patients/history", params=params)
        if response.status_code == 200:
            df = pd.DataFrame(response.json()["data"])
            st.dataframe(df, use_container_width=True)
        else:
            st.error(response.json())

elif menu == "Doctor Workload":
    st.header("View Doctor Workload")
    doctor_id = st.text_input("Doctor ID")
    if st.button("Search"):
        params = {
            "doctor_id": doctor_id
        }
        response = requests.get(f"{BASE_URL}/doctors/workload", params=params)
        if response.status_code == 200:
            df = pd.DataFrame(response.json()["data"])
            st.dataframe(df, use_container_width=True)
        else:
            st.error(response.json())   

            
         


    