import streamlit as st
import requests
import pandas as pd
from datetime import date
import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from datetime import date
from streamlit_calendar import calendar


BASE_URL = "http://127.0.0.1:8000"

st.markdown("""
<style>

.main {
    background-color: #f5f7fa;
}
.block-container {
    padding-top: 1.8rem;
    padding-bottom: 2rem;
}
[data-testid="metric-container"] {
    background: white;
    border-radius: 15px;
    padding: 18px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
    border-left: 5px solid #4F8BF9;
}
.chart-card {
    background: white;
    padding: 2px;
    border-radius: 18px;
    box-shadow: 0px 4px 14px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}
.heading {
    font-size: 40px;
    font-weight: 700;
    color: #1E293B;
    text-align: center;
    margin-bottom: -30px;
}
.info{
    font-size: 18px;
    font-weight: 600;
    color: #1E293B;
    margin-bottom: 10px;
}
.section-title {
    font-size: 26px;
    font-weight: 700;
    color: #1E293B;
    margin-bottom: 10px;
}
.small-title {
    font-size: 10px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

st.set_page_config(
    page_title="Hospital Management System",
    layout="wide"
)
st.markdown('<div class="heading">Hospital Management System Dashboard</div>', unsafe_allow_html=True)
# st.info("Use the sidebar to manage hospital records.")
st.divider()

menu = st.sidebar.radio(
    "Hospital Modules",
    [
        "Home",
        "Patients",
        "Doctors",
        "Appointments",
        "Treatments",
        "Billing",
        "Analytics"
    ]
)
#chatbot
st.sidebar.title("AI Assistant")
query = st.sidebar.text_input("Ask me anything")
if st.sidebar.button("Ask"):
    payload = {
        "query": query
    }
    response = requests.post(f"{BASE_URL}/chatbot", json=payload)
    if response.status_code==200:
        answer = response.json()
        st.sidebar.write(answer["response"])
    else:
        st.sidebar.error(response.text)















if menu == "Home":
   
    #Fetch Data From APIs
    patients = requests.get(f"{BASE_URL}/patients/show all records").json()["data"]
    doctors = requests.get(f"{BASE_URL}/doctors/show all records").json()["data"]
    appointments = requests.get(f"{BASE_URL}/appointments/all").json()["data"]
    treatments = requests.get(f"{BASE_URL}/treatments/all").json()["data"]
    billing = requests.get(f"{BASE_URL}/billing/all").json()["data"]
    #Convert to DataFrames
    patients_df = pd.DataFrame(patients)
    doctors_df = pd.DataFrame(doctors)
    appointments_df = pd.DataFrame(appointments)
    treatments_df = pd.DataFrame(treatments)
    billing_df = pd.DataFrame(billing)
    #Add KPI Metric Cards
    total_patients = len(patients_df)
    total_doctors = len(doctors_df)
    total_appointments = len(appointments_df)
    total_treatments = len(treatments_df)
    total_billing = billing_df["amount"].sum()

    st.markdown('<div class="info">', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Patients", total_patients)
    with col2:
        st.metric("Total Appointments", total_appointments)
    with col3:
        st.metric("Total Doctors", total_doctors)
    with col4:
        st.metric("Total Treatments", total_treatments)
    st.markdown('</div>', unsafe_allow_html=True)

    #Add Charts
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    st.markdown(
            '<div class="chart-card">',
            unsafe_allow_html=True
        )
    with col1:
        st.markdown("<div class='info'>Patients by Gender</div>", unsafe_allow_html=True)
        patients_by_gender = patients_df["gender"].value_counts()
        st.bar_chart(patients_by_gender)
    with col2:
        st.markdown("<div class='small-title'>Doctors by Specialization</div>", unsafe_allow_html=True)
        doctors_by_specialization = doctors_df["specialization"].value_counts()
        st.bar_chart(doctors_by_specialization)
    with col3:
        st.subheader("Appointments by Status")
        appointments_by_status = appointments_df["status"].value_counts()
        st.bar_chart(appointments_by_status)
    with col4:
        st.subheader("Treatments by Type")
        treatments_by_type = treatments_df["treatment_type"].value_counts()
        st.bar_chart(treatments_by_type)
    with col5:
        st.subheader("Billing by Payment Method")
        billing_by_payment_method = billing_df["payment_method"].value_counts()
        st.bar_chart(billing_by_payment_method)
    with col6:
        st.subheader("Billing by Payment Status")
        billing_by_payment_status = billing_df["payment_status"].value_counts()
        st.bar_chart(billing_by_payment_status)
    st.markdown('</div>', unsafe_allow_html=True)

    pending_count = len(billing_df[billing_df["payment_status"] == "Pending"])
    paid_count = len(
        billing_df[
            billing_df["payment_status"] == "Paid"
        ]
    )
    cancelled_count = len(
        billing_df[
            billing_df["payment_status"] == "Failed"
        ]
    )
    st.subheader("Payment Status")
    col1, col2, col3 = st.columns(3)
    with col1:
        payment_fig=px.pie(billing_df, names="payment_status", title="Payment Dsitribution")
        st.plotly_chart(payment_fig, use_container_width=True)
    col3.warning(f"Pending Bills: {pending_count}")
    col3.success(f"Paid Bills: {paid_count}")
    col3.error(f"Failed Bills: {cancelled_count}")

    #revenue line chart
    st.subheader("Revenue Trend")
    billing_df["bill_date"] = pd.to_datetime(billing_df["bill_date"])
    revenue_by_date = px.bar(
        billing_df,
        x="bill_date",
        y="amount",
        title="Revenue Over Time",
        labels={
            "bill_date": "Date",
            "amount": "Revenue"
        }       
    )
    st.plotly_chart(revenue_by_date, use_container_width=True)
    st.metric("Total Revenue", total_billing)

    #Treatment analytics
    st.subheader("Treatment Analytics")
    treatment_count = (treatments_df["treatment_type"].value_counts().reset_index())
    treatment_count.columns = ["Treatment Type", "Count"]
    st.dataframe(treatment_count, use_container_width=True)
    fig = px.bar(
        treatment_count,
        x="Treatment Type",
        y="Count",
        title="Top Treatments")
    st.plotly_chart(fig, use_container_width=True)

    #Appointments
    calender_events = []
    for _, row in appointments_df.iterrows():
        calender_events.append({
            "title":row["reason_for_visit"],
            "start":row["appointment_date"],
            "end":row["appointment_time"]
        })
    st.subheader("Appointments Calendar")
    calendar_options = {"initialView": "dayGridMonth"}
    calendar(events=calender_events, options=calendar_options)

    appointments_df["appointment_date"] = pd.to_datetime(
    appointments_df["appointment_date"]
    )
    appointments_df["day"] = appointments_df[
        "appointment_date"
    ].dt.day_name()
    heatmap = appointments_df.groupby(
        ["day", "doctor_id"]
    ).size().reset_index(name="count")
    heatmap_fig = px.density_heatmap(
        heatmap,
        x="day",
        y="doctor_id",
        z="count",
        title="Appointments Heatmap"
    )
    st.plotly_chart(heatmap_fig, use_container_width=True)



    #Doctor Workload
    response = requests.get(f"{BASE_URL}/doctors/workload")
    if response.status_code != 200:
        st.error(response.text)
    else:
        workload = response.json()
        workload_df = pd.DataFrame(workload["data"])
        st.subheader("Doctor Workload")
        st.dataframe(workload_df, use_container_width=True)
        col1, col2 = st.columns(2)
        with col1:
            doctor_fig = px.bar(
            workload_df,
            x="doctor_name",
            y="total_appointments",
            color="total_appointments",
            title="Appointments per Doctor"
            )
            st.plotly_chart(doctor_fig, use_container_width=True)
        with col2:
            pie_fig = px.pie(
                workload_df,
                names="doctor_name",
                values="total_appointments",
                title="Appointments per Doctor")

            st.plotly_chart(pie_fig, use_container_width=True)
 
elif menu == "Patients":

    action = st.selectbox(
        "Patient Actions",
        [
            "Add Patient",
            "Search Patient",
            "Update Patient",
            "Delete Patient"        ]
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
            if not first_name.strip():
                st.error("First name is required")
            elif not contact_number.isdigit():
                st.error("Required Contact number must be a numeric")
            elif len(contact_number) != 10:
                st.error("Contact number must be 10 digits")
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
            response = requests.post(f"{BASE_URL}/patients", json=params)
            if response.status_code == 200:
                st.success("Patient created successfully")
                st.json(response.json())
            else:
                error_data = response.json()
                if "errors" in error_data:
                    for error in error_data["errors"]:
                        st.error(f"{error['field']}: {error['message']}")
                else:
                    st.error(error_data)

    elif action == "Search Patient":
        st.subheader("Search Patient")
        patient_id = st.text_input("Patient ID")
        first_name = st.text_input("First Name")
        if st.button("Search"):
            if not patient_id.strip():
                st.error("Patient ID is required")
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
        gender = st.selectbox("Gender", ["M", "F"])
        date_of_birth = st.date_input("Date of Birth", min_value=date(1900,1,1), max_value=date.today())
        contact_number = st.text_input("Contact Number")
        address = st.text_input("Address")
        insurance_provider = st.text_input("Insurance Provider")
        insurance_number = st.text_input("Insurance Number")
        email = st.text_input("Email")
        if st.button("Update"):
            if not patient_id.strip():
                st.error("Patient ID is required")
            
            params = {"patient_id": patient_id, "first_name": first_name, "last_name": last_name, "gender": gender, "date_of_birth": date_of_birth, "contact_number": contact_number, "address": address, "insurance_provider": insurance_provider, "insurance_number": insurance_number, "email": email }
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
            if not patient_id.strip():
                st.error("Patient ID is required")
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
    action = st.selectbox(
        "Doctor Actions",
        [
            "Search Doctor",
            "Update Doctor"
        ]
    )
    if action == "Search Doctor":
        st.subheader("Search Doctor")
        doctor_id = st.text_input("Doctor ID")
        first_name = st.text_input("Doctor First Name")
        specialization = st.text_input("Specialization")
        if st.button("Search"):
            if not doctor_id.strip():
                st.error("Doctor ID is required")
            params = {
                "doctor_id": doctor_id,
                "first_name": first_name,
                "specialization": specialization
            }
            response = requests.get(f"{BASE_URL}/doctors", params=params)
            if response.status_code==200:
                df = pd.DataFrame(response.json()["data"])
                st.dataframe(df, use_container_width=True)
            else:
                st.error(response.json())

    elif action == "Update Doctor":
        st.subheader("Update Doctor")
        doctor_id = st.text_input("Doctor ID")
        first_name = st.text_input("Doctor First Name")
        last_name = st.text_input("Doctor Last Name")
        specialization = st.text_input("Specialization")
        phone_number = st.text_input("Phone Number")
        years_experience = st.text_input("Years of experience")
        hospital_branch = st.text_input("Hospital Branch")
        email = st.text_input("Email")
        if st.button("Update"):
            if not doctor_id.strip():
                st.error("Doctor ID is required")
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
            "Update Appointment",
            "Delete Appointment"
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
            if not patient_id.strip():
                st.error("Patient ID is required")
            elif not doctor_id.strip():
                st.error("Doctor ID is required")
            elif not reason_for_visit.strip():
                st.error("Reason for visit is required")
            
            params = {
                "patient_id": patient_id,
                "doctor_id": doctor_id,
                "appointment_date": str(appointment_date),
                "appointment_time": str(appointment_time),
                "reason_for_visit": reason_for_visit
            }
            response = requests.post(f"{BASE_URL}/appointments", json=params)
            if response.status_code == 200:
                st.toast("New appointment created")
                st.json(response.json())
            else:
                error_data = response.json()
                if "errors" in error_data:
                    for err in error_data["errors"]:
                        st.error(f"{err['field']}: {err['message']}")
                else:
                    st.error(error_data)

    if action == "Search Appointment":
        st.subheader("Search Appointment")
        appointment_id = st.text_input("Appointment ID")
        first_name = st.text_input("Patient First Name")
        if st.button("Search"):
            if not appointment_id.strip():
                st.error("Appointment ID is required")
            
            params = { 
                "appointment_id": appointment_id,
                "first_name": first_name
            }
            response = requests.get(f"{BASE_URL}/appointments/search", params=params)
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
            if not appointment_id.strip():
                st.error("Appointment ID is required")
            
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
    
    if action == "Delete Appointment":
        st.subheader("Delete Appointment")
        appointment_id = st.text_input("Appointment ID")
        if st.button("Delete"):
            if not appointment_id.strip():
                st.error("Appointment ID is required")
            
            params = {
                "appointment_id": appointment_id
            }
            response = requests.delete(f"{BASE_URL}/appointments", params=params)
            if response.status_code == 200:
                st.success("Appointment deleted successfully")
                st.json(response.json())
            else:
                st.error(response.json())
                
elif menu == "Treatments":
    action = st.selectbox(
        "Treatment Actions",
        [
            "Create Treatment",
            "Search Treatment"
        ]
    )
    if action == "Create Treatment":
        st.subheader("Create Treatment")
        appointment_id = st.text_input("Appointment ID")
        treatment_date = st.date_input("Treatment Date", min_value=date.today())
        #fetch treatment options
        response = requests.get(f"{BASE_URL}/treatment-options")
        options = response.json()["data"]
        treatment_map = {
            f"{item['treatment_type']} - {item['description']}": item
            for item in options
        }
        selected = st.selectbox(
            "Select Treatment",
            list(treatment_map.keys())
        )
        selected_data = treatment_map[selected]
        treatment_type = selected_data["treatment_type"]
        description = selected_data["description"]
        cost = selected_data["cost"]
        st.info(f"Cost: {cost}")

        if st.button("Create"):
            if not appointment_id.strip():
                st.error("Appointment ID is required")
            elif not treatment_type.strip():
                st.error("Treatment Type is required")
            elif not description.strip():
                st.error("Description is required")
            
            params = {
                "appointment_id": appointment_id,
                "description": description,
                "treatment_type": treatment_type,
                "treatment_date": str(treatment_date)
            }
    
            response = requests.post(f"{BASE_URL}/treatments", json=params)
            if response.status_code == 200:
                st.success("Treatment created successfully")
                st.json(response.json())
            else:
                error_data = response.json()
                if "errors" in error_data:
                    for err in error_data["errors"]:
                        st.error(f"{err['field']}: {err['message']}")
                else:
                    st.error(error_data)

    if action == "Search Treatment":
        st.subheader("Search Treatment")
        treatment_id = st.text_input("Treatment ID")
        treatment_type = st.text_input("Treatment Type")
        if st.button("Search"):
            if not treatment_id.strip():
                st.error("Treatment ID is required")
            
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
                

    if action == "Delete Treatment":
        st.subheader("Delete Treatment")
        treatment_id = st.text_input("Treatment ID")
        if st.button("Delete"):
            if not treatment_id.strip():
                st.error("Treatment ID is required")
            
            params = {
                "treatment_id": treatment_id
            }
            response = requests.put(f"{BASE_URL}/treatments", params=params)
            if response.status_code == 200:
                st.success("Treatment deleted successfully")
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
            if not bill_id.strip():
                st.error("Bill ID is required")
            
            params = {
                    "bill_id": bill_id,
                    "patient_id": patient_id
                }
            response = requests.get(f"{BASE_URL}/billing/search", params=params)
            if response.status_code == 200:
                df = pd.DataFrame(response.json()["data"])
                st.dataframe(df, use_container_width=True)
            else:
                st.error(response.json())

    if action == "Update Billing":
        st.subheader("Update Billing")
        bill_id = st.text_input("Bill ID")
        amount = st.number_input("Amount", min_value=0.0, step=100.0)
        payment_date = st.date_input("Payment Date")
        payment_method = st.selectbox("Payment Method", ["Cash", "Credit Card", "Debit Card", "Bank Transfer"])
        payment_status = st.selectbox("Payment Status", ["Pending", "Paid", "Failed"])
        if st.button("Update"):
            if not bill_id.strip():
                st.error("Bill ID is required")
            elif not amount and amount<0:
                st.error("Amount is required and cannot be negative")
            elif not payment_date:
                st.error("Payment Date is required")
            
            params = {
                "bill_id": bill_id,
                "amount": amount,
                "payment_date": str(payment_date),
                "payment_method": payment_method,
                "payment_status": payment_status
            }            
            response = requests.put(f"{BASE_URL}/billing/{bill_id}", json=params)
            if response.status_code == 200:
                st.success("Billing updated successfully")
                st.json(response.json())
            else:
                st.error(response.json())

elif menu == "Analytics":
    st.header("View Patient History")
    patient_id = st.text_input("Patient ID")
    if st.button("Fetch History"):
        if not patient_id.strip():
            st.error("Patient ID is required")
        
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

            
#