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
st.set_page_config(
    page_title="Hospital Management System",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.main {
    background-color: #0F172A;
    color: #00000
}
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    padding-left: 2rem;
    padding-right: 2rem;
}
.heading {
    font-size: 40px;
    font-weight: 700;
    color: #F8FAFC;
    text-align: center;
    margin-bottom: -30px;
}
.sub-header {
    font-size: 24px;
    font-weight: 600;
    color: #E2E8F0;
    margin-bottom: 15px;
    text-align: center;
}
.info {
    font-size: 18px;
    font-weight: 600;
    color: #F8FAFC;
    text-align: center;
    margin-bottom: 10px;
}

/* =========================
METRIC CARDS
========================= */

[data-testid="stMetric"] {

    background: linear-gradient(
        135deg,
        #1E293B,
        #0F172A
    );

    border: 1px solid #334155;

    padding: 18px;

    border-radius: 16px;

    text-align: center;

    box-shadow:
        0 4px 12px rgba(0,0,0,0.35);

}

/* Metric label */

[data-testid="stMetricLabel"] {
    color: #CBD5E1;
    font-size: 12px;
    text-align: center;
}

/* Metric value */

[data-testid="stMetricValue"] {
    color: #F8FAFC;
    font-size: 16px;
    font-weight: 500;
}

/* =========================
CHART CONTAINERS
========================= */

.chart-card {

    background-color: #111827;

    padding: 18px;

    border-radius: 16px;

    border: 1px solid #334155;

    margin-bottom: 20px;

    box-shadow:
        0 4px 12px rgba(0,0,0,0.25);
}

/* =========================
BUTTONS
========================= */

.stButton > button {

    background-color: #2563EB;

    color: white;

    border-radius: 10px;

    border: none;

    padding: 10px 18px;

    font-weight: 600;

    transition: 0.3s;
}

.stButton > button:hover {

    background-color: #1D4ED8;

    color: white;

    border: none;
}

/* =========================
INPUT FIELDS
========================= */

.stTextInput input,
.stNumberInput input,
.stDateInput input,
textarea {

    background-color: #1E293B !important;

    color: #F8FAFC !important;

    border-radius: 10px !important;

    border: 1px solid #475569 !important;
}

/* Selectbox */

.stSelectbox div[data-baseweb="select"] {

    background-color: #1E293B !important;

    border-radius: 10px !important;

    border: 1px solid #475569 !important;
}

/* =========================
DATAFRAMES
========================= */

[data-testid="stDataFrame"] {

    background-color: #111827;

    border-radius: 12px;

    padding: 10px;

    border: 1px solid #334155;
}

/* =========================
SUCCESS / ERROR BOXES
========================= */

.stSuccess {
    background-color: rgba(34,197,94,0.15);
}

.stError {
    background-color: rgba(239,68,68,0.15);
}

.stWarning {
    background-color: rgba(245,158,11,0.15);
}
.info {
    background-color: rgba(59,130,246,0.15);
}
section[data-testid="stSidebar"] {
    background-color: #111827;
    border-right: 1px solid #334155;
}
section[data-testid="stSidebar"] * {
    color: #F8FAFC;
}
</style>""", unsafe_allow_html=True)

menu = st.sidebar.radio(
    "HOSPITAL MODULES",
    [
        "Home",
        "Patients",
        "Doctors",
        "Appointments",
        "Treatments",
        "Billing",
        "Patient History",
        "Doctor Workload",
        "Appointments Calendar",
        "Hospital Catalog"
    ]
)

st.sidebar.divider()

#chatbot
st.sidebar.title("AI Assistant Desk")
query = st.sidebar.text_input("Ask me anything")
if st.sidebar.button("Ask"):
    if not query.strip():
        st.sidebar.error("Please enter a query")
    else:
        payload = {
            "query": query
        }
        response = requests.post(f"{BASE_URL}/chatbot", json=payload)
        if response.status_code==200:
            answer = response.json()
            st.sidebar.success(answer["response"])
        else:
            st.sidebar.error(response.text)

if menu == "Home":
    st.markdown('<div class="heading">Hospital Management System Dashboard</div>', unsafe_allow_html=True)
# st.info("Use the sidebar to manage hospital records.")
    st.divider()
   
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

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Total Patients", total_patients)
    with col2:
        st.metric("Total Appointments", total_appointments)
    with col3:
        st.metric("Total Doctors", total_doctors)
    with col4:
        st.metric("Total Treatments", total_treatments)
    with col5:
        st.metric("Total Billing", total_billing)

    #Add Charts
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='info'>Patient Analytics</div>", unsafe_allow_html=True)
        patients_df['gender'] = patients_df['gender'].replace({'M': 'Male', 'F': 'Female'})
        patients_by_gender = patients_df["gender"].value_counts().reset_index()
        patients_by_gender.columns = ["Gender", "Count"]
        gender_fig=px.bar(patients_by_gender, x="Gender", y="Count",text_auto=True, template="plotly_dark")
        gender_fig.update_layout(height=300, margin=dict(t=0, b=10, l=10, r=0))
        st.plotly_chart(gender_fig, use_container_width=True)
    with col2:
        st.markdown("<div class='info'>Doctor Analytics</div>", unsafe_allow_html=True)
        doctors_by_specialization = doctors_df["specialization"].value_counts().reset_index()
        doctors_by_specialization.columns = ["Specialization", "Count"]
        specialization_fig=px.bar(doctors_by_specialization, x="Specialization", y="Count",text_auto=True, template="plotly_dark")
        specialization_fig.update_layout(height=300, margin=dict(t=0, b=10, l=10, r=0))
        st.plotly_chart(specialization_fig, use_container_width=True)

    # with col3:
    #     st.markdown("<div class='info'>Appointments by Status</div>", unsafe_allow_html=True)
    #     appointments_by_status = appointments_df["status"].value_counts()
    #     st.bar_chart(appointments_by_status)
    # with col1:
    #     st.markdown("<div class='info'>Treatments by Type</div>", unsafe_allow_html=True)
    #     treatments_by_type = treatments_df["treatment_type"].value_counts()
    #     st.bar_chart(treatments_by_type)
    with col3:
        st.markdown("<div class='info'>Payment Analytics</div>", unsafe_allow_html=True)
        billing_by_payment_method=billing_df["payment_method"].value_counts().reset_index()
        billing_by_payment_method.columns=["Payment Method","Count"]
        payment_fig=px.bar(billing_by_payment_method, x="Payment Method", y="Count",text_auto=True, template="plotly_dark")
        payment_fig.update_layout(height=300, margin=dict(t=0, b=10, l=10, r=0))
        st.plotly_chart(payment_fig, use_container_width=True)
    # with col3:
    #     st.markdown("<div class='info'>Billing by Payment Status</div>", unsafe_allow_html=True)
    #     billing_by_payment_status = billing_df["payment_status"].value_counts()
    #     st.bar_chart(billing_by_payment_status)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='info'>Appointment Analytics</div>", unsafe_allow_html=True)
        appointments_fig=px.pie(appointments_df, names="status")
        appointments_fig.update_layout(height=300, margin=dict(t=10, b=10, l=10, r=10))
        st.plotly_chart(appointments_fig, use_container_width=True)
    with col2:
        st.markdown("<div class='info'>Billing Analytics</div>", unsafe_allow_html=True)   
        pending_count = len(billing_df[billing_df["payment_status"] == "Pending"])
        paid_count = len(        billing_df[            billing_df["payment_status"] == "Paid"        ]        )
        cancelled_count = len(        billing_df[            billing_df["payment_status"] == "Failed"        ]        )   
        col2.warning(f"Pending Bills: {pending_count}")
        col2.success(f"Paid Bills: {paid_count}")
        col2.error(f"Failed Bills: {cancelled_count}")
    with col3:
        st.markdown("<div class='info'>Treatment Analytics</div>", unsafe_allow_html=True)
        treatment_fig=px.pie(treatments_df, names="treatment_type")
        treatment_fig.update_layout(height=300, margin=dict(t=0, b=10, l=10, r=0))
        st.plotly_chart(treatment_fig, use_container_width=True)


    st.markdown("<div class='info'>Treatment Catalog Analytics</div>", unsafe_allow_html=True)

    # Fetch treatment catalog
    catalog_response = requests.get(f"{BASE_URL}/treatment-options")

    if catalog_response.status_code == 200:

        catalog_df = pd.DataFrame(
            catalog_response.json()["data"]
        )
        col1,col2 = st.columns(2)
        with col1:
            st.markdown("<div class='small-title'>Patients per Treatment</div>", unsafe_allow_html=True)
            # Count treatments by description
            treatment_desc_df = (
                treatments_df.groupby(
                    ["treatment_type", "description"]
                )
                .size()
                .reset_index(name="patient_count")
            )

            # Treemap visualization
            treemap_fig = px.treemap(
                treatment_desc_df,
                path=[
                    "treatment_type",
                    "description"
                ],
                values="patient_count",
            )

            treemap_fig.update_layout(
                margin=dict(t=40, l=10, r=10, b=10),
                height=400,
            )

            st.plotly_chart(
                treemap_fig,
                use_container_width=True
            )
            # Treemap Visual
            # treatment_cost_fig = px.treemap(
            #     catalog_df,
            #     path=["treatment_type", "description"],
            #     values="cost",
            #     color="cost",
            #     hover_data=["cost"],
            #     title="Treatment Types, Descriptions & Cost Distribution"
            # )

            # st.plotly_chart(
            #     treatment_cost_fig,
            #     use_container_width=True
            # )
            
        with col2:
            st.markdown("<div class='small-title'>Cost per Treatment</div>", unsafe_allow_html=True)
            # Bar Chart
            
            catalog_df["label"] = (            catalog_df["treatment_type"]
            + " - "
            + catalog_df["description"]            )
            cost_fig = px.bar(
                catalog_df,
                x="cost",
                y="label",
                orientation="h",
                color="cost",
            )
            cost_fig.update_layout(
                height=400,
                yaxis_title="Treatment",
                xaxis_title="Cost"
            )
            st.plotly_chart(cost_fig, use_container_width=True)
    else:
        st.error("Could not load treatment catalog")

    # with col3:

    #     doctor_fig = px.bar(
    #         appointments_df,
    #         x="doctor_id",
    #         color="status",
    #         title="Doctor Appointment Load"
    #     )

    #     doctor_fig.update_layout(height=300)

    #     st.plotly_chart(
    #         doctor_fig,
    #         use_container_width=True
    #     )

    #revenue line chart
    st.markdown("<div class='info'>Revenue Analytics</div>", unsafe_allow_html=True)
    billing_df["bill_date"] = pd.to_datetime(billing_df["bill_date"])
    revenue_by_date = px.bar(
        billing_df,
        x="bill_date",
        y="amount",
        labels={
            "bill_date": "Date",
            "amount": "Revenue"
        }       
    )
    st.plotly_chart(revenue_by_date, use_container_width=True)

elif menu == "Patients":
    st.header("Patient Records")

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
                st.stop()
            elif not contact_number.isdigit():
                st.error("Required Contact number must be a numeric")
                st.stop()
            elif len(contact_number) != 10:
                st.error("Contact number must be 10 digits")
                st.stop()
            
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
                st.stop()
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
                st.stop()
           
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
                st.stop()
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
                st.stop()
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
                st.stop()
            
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
    st.header("Appointment Records")
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
                st.stop()
            elif not doctor_id.strip():
                st.error("Doctor ID is required")
                st.stop()
            elif not reason_for_visit.strip():
                st.error("Reason for visit is required")
                st.stop()
            
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
                st.stop()
            
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
                st.stop()
            elif not status.strip():
                st.error("Status is required")
                st.stop()
            
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
                st.stop()
            
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
    st.header("Treatment Records")
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
                st.stop()
            elif not treatment_type.strip():
                st.error("Treatment Type is required")
                st.stop()
            elif not description.strip():
                st.error("Description is required")
                st.stop()
            
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
                st.stop()
            
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
                st.stop()
            
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
    st.header("Billing Records")
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
                st.stop()
            
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
                st.stop()
            elif not amount and amount<0:
                st.error("Amount is required and cannot be negative")
                st.stop()
            elif not payment_date:
                st.error("Payment Date is required")
                st.stop()
            
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

elif menu == "Patient History":
    st.header("View Patient History")
    patient_id = st.text_input("Patient ID")
    if st.button("Fetch History"):
        if not patient_id.strip():
            st.error("Patient ID is required")
            st.stop()        
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
    #Doctor Workload
    response = requests.get(f"{BASE_URL}/doctors/workload")
    if response.status_code != 200:
        st.error(response.text)
    else:
        workload = response.json()
        workload_df = pd.DataFrame(workload["data"])
        st.dataframe(workload_df, use_container_width=True)
        doctor_fig = px.bar(
        workload_df,
        x="doctor_name",
        y="total_appointments",
        color="total_appointments",
        title="Appointments per Doctor"            )
        st.plotly_chart(doctor_fig, use_container_width=True) 

elif menu == "Appointments Calendar":

    st.header("Appointments Calendar")
    # FETCH APPOINTMENTS
    response = requests.get(
        f"{BASE_URL}/appointments/details"
    )
    if response.status_code != 200:

        st.error(response.text)

    else:

        data = response.json()

        appointments = data.get("data", [])

        if not appointments:

            st.warning("No appointments available")

        else:

            # =========================
            # CREATE CALENDAR EVENTS
            # =========================

            events = []

            for row in appointments:

                events.append({
                    "title": (
                        f"{row['patient_name']} - "
                        f"{row['reason_for_visit']}"
                    ),

                    "start": str(
                        row["appointment_date"]
                    ),

                    "id": row["appointment_id"]
                })

            # SHOW CALENDAR
            calendar_data = calendar(
                events=events,
                options={
                    "initialView": "dayGridMonth",
                    "height": 700,
                    "headerToolbar": {
                        "left": "prev,next today",
                        "center": "title",
                        "right": (
                            "dayGridYear,"
                            "dayGridMonth,"
                            "timeGridWeek,"
                            "timeGridDay"
                        )
                    }
                },

                key="appointments-calendar"
            )
            # EVENT CLICK DETAILS
            if (
                calendar_data
                and calendar_data.get("eventClick")
            ):

                selected_id = (
                    calendar_data["eventClick"]
                    ["event"]["id"]
                )

                detail_response = requests.get(
                    f"{BASE_URL}/appointments/details",
                    params={
                        "appointment_id": selected_id
                    }
                )

                if detail_response.status_code == 200:

                    detail_data = (
                        detail_response.json()
                    )

                    details = detail_data.get(
                        "data",
                        {}
                    )

                    st.divider()

                    st.subheader(
                        "Appointment Details"
                    )

                    col1, col2 = st.columns(2)

                    with col1:

                        st.info(
                            f"Patient: "
                            f"{details.get('patient_name', 'N/A')}"
                        )

                        st.info(
                            f"Doctor: "
                            f"{details.get('doctor_name', 'N/A')}"
                        )

                        st.info(
                            f"Appointment ID: "
                            f"{details.get('appointment_id', 'N/A')}"
                        )

                        st.info(
                            f"Visit Reason: "
                            f"{details.get('reason_for_visit', 'N/A')}"
                        )

                    with col2:

                        st.success(
                            f"Treatment: "
                            f"{details.get('treatment_type', 'N/A')}"
                        )

                        st.success(
                            f"Billing Amount: "
                            f"{details.get('amount', 'N/A')}"
                        )

                        st.success(
                            f"Payment Status: "
                            f"{details.get('payment_status', 'N/A')}"
                        )

                        st.success(
                            f"Appointment Date: "
                            f"{details.get('appointment_date', 'N/A')}"
                        )

                else:

                    st.error(
                        "Could not fetch appointment details"
                    )   

elif menu == "Hospital Catalog":
    st.header("Hospital Catalog")
    response = requests.get(f"{BASE_URL}/hospital-catalog")
    if response.status_code != 200:
        st.error(response.text)
    else:
        catalog = response.json()
        catalog_df = pd.DataFrame(catalog["data"])
        st.dataframe(catalog_df, use_container_width=True)
    
        # search = st.text_input("Search Catalog")
        # if search:
        #     catalog_df = catalog_df[
        #         catalog_df.astype(str)
        #     .apply(
        #         lambda row:
        #         row.str.contains(
        #             search, 
        #             case=False
        #         ).any(),
        #         axis =1
        #     )]