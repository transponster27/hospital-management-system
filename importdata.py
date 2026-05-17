import pandas as pd
from psycopg2.extras import execute_batch
from database import get_connection

DATA_PATH = "csv_files/"

def clean_df(df):
    df = df.drop_duplicates()
    df = df.where(pd.notnull(df), None)
    return df

def insert_data():

    conn = get_connection()
    cur = conn.cursor()

    try:

        #  PATIENTS 
        patients = clean_df(pd.read_csv(DATA_PATH + "patients.csv"))

        execute_batch(cur, """
            INSERT INTO patients (
                patient_id, first_name, last_name, gender,
                date_of_birth, contact_number, address,
                registration_date, insurance_provider,
                insurance_number, email
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, patients.values.tolist())                      #List of rows

        conn.commit()

        #  DOCTORS 
        doctors = clean_df(pd.read_csv(DATA_PATH + "doctors.csv"))

        execute_batch(cur, """
            INSERT INTO doctors (
                doctor_id, first_name, last_name,
                specialization, phone_number,
                years_experience, hospital_branch, email
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """, doctors.values.tolist())

        conn.commit()

        #  APPOINTMENTS 
        appointments = clean_df(pd.read_csv(DATA_PATH + "appointments.csv"))

        execute_batch(cur, """
            INSERT INTO appointments (
                appointment_id, patient_id, doctor_id,
                appointment_date, appointment_time,
                reason_for_visit, status
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s)
        """, appointments.values.tolist())

        conn.commit()

        #  TREATMENTS 
        treatments = clean_df(pd.read_csv(DATA_PATH + "treatments.csv"))

        execute_batch(cur, """
            INSERT INTO treatments (
                treatment_id, appointment_id,
                treatment_type, description,
                cost, treatment_date
            )
            VALUES (%s,%s,%s,%s,%s,%s)
        """, treatments.values.tolist())

        conn.commit()

        #  BILLING 
        billing = clean_df(pd.read_csv(DATA_PATH + "billing.csv"))

        execute_batch(cur, """
            INSERT INTO billing (
                bill_id, patient_id, treatment_id,
                bill_date, amount,
                payment_method, payment_status
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s)
        """, billing.values.tolist())

        conn.commit()

        print("Data import completed successfully.")

    except Exception as e:
        conn.rollback()
        print("Error:", e)

    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    insert_data()