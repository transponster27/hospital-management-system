from fastapi import FastAPI, Request, HTTPException, Query
from database import get_connection
from psycopg2.extras import RealDictCursor
from datetime import date

app = FastAPI(title="Hospital Management API")

@app.get("/")
def home():
    return {"message": "Hospital Database API Running"}

#add new patient
@app.post("/patients")
def create_patient(
    first_name: str,
    last_name: str,
    gender: str,
    date_of_birth: str,
    contact_number: str = None,
    address: str = None,
    insurance_provider: str = None,
    insurance_number: str = None,
    email: str = None
):
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        #generate p_id
        cur.execute("""
            SELECT patient_id
            FROM patients
            ORDER BY patient_id DESC
            LIMIT 1;
            """)
        last_patient = cur.fetchone()
        print(last_patient)
        if last_patient:
            last_num = int(last_patient["patient_id"][1:])
            patient_id = f"P{last_num + 1:03d}"
        else:
            patient_id = "P001"      
        #insert patient
        query = """
            INSERT INTO patients (
                patient_id,
                first_name,
                last_name,
                gender,
                date_of_birth,
                contact_number,
                address,
                insurance_provider,
                insurance_number,
                email
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            RETURNING *;
        """
        cur.execute(query, (
            patient_id,
            first_name,
            last_name,
            gender,
            date_of_birth,
            contact_number,
            address,
            insurance_provider,
            insurance_number,
            email
        ))
        conn.commit()
        new_patient = cur.fetchone()
        cur.close()
        conn.close()
        return {
            "status": "created",
            "data": new_patient
        }
    except Exception as e:
        if conn:
            conn.rollback()
            conn.close()
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

#search a patient
@app.get("/patients")
def search_patient(
    patient_id: str = None,
    first_name: str = None
):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        query = "SELECT * FROM patients"
        conditions = []
        params = []
        if patient_id:
            conditions.append("LOWER(patient_id) = LOWER(%s)")
            params.append(patient_id)
        if first_name:
            conditions.append("LOWER(first_name) LIKE LOWER(%s)")
            params.append(f"{first_name}")
        if conditions:
            print(conditions)
            query += " WHERE " + " AND ".join(conditions)
            print(query)
        cur.execute(query, tuple(params))
        rows = cur.fetchall()
        if not rows:
            raise HTTPException(status_code=404, detail="Patient not found")
        return {"count": len(rows), "data": rows}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cur.close()
        conn.close()    
        
#get all patients   
@app.get("/patients/show all records")
def get_patients():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:   
        cur.execute("SELECT * FROM patients;")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return {"data":rows}
    except Exception as e:
        return {"error": str(e)}
    finally:
        cur.close()
        conn.close()

#update
@app.put("/patients")
def update_patient(
    patient_id: str,
    first_name: str=None,
    last_name: str=None,
    gender: str=None,
    date_of_birth: str=None,
    contact_number: str=None,
    address: str=None,
    registration_date: str=None,
    insurance_provider: str=None,
    insurance_number: str=None,
    email: str=None):
    conn = get_connection()
    cur = conn.cursor(cursor_factory= RealDictCursor)
    try:
        updates = []
        params = []
        if first_name:
            updates.append("first_name = %s")
            params.append(first_name)
        if last_name:
            updates.append("last_name = %s")
            params.append(last_name)
        if gender:
            updates.append("gender = %s")
            params.append(gender)
        if date_of_birth:
            updates.append("date_of_birth = %s")
            params.append(date_of_birth)
        if contact_number:
            updates.append("contact_number = %s")
            params.append(contact_number)
        if address:
            updates.append("address = %s")
            params.append(address)
        if registration_date:
            updates.append("registration_date = %s")
            params.append(registration_date)
        if insurance_provider:
            updates.append("insurance_provider = %s")
            params.append(insurance_provider)
        if insurance_number:
            updates.append("insurance_number = %s")
            params.append(insurance_number)
        if email:
            updates.append("email = %s")
            params.append(email)
        if not updates:
            raise HTTPException(status_code=400, details= "No field to update")
        print(updates)
        print(params)
        query= f"""
            UPDATE patients
            SET {", ".join(updates)}
            WHERE LOWER(patient_id) = LOWER(%s)
            RETURNING *;
            """
        params.append(patient_id)
        cur.execute(query, tuple(params))
        updated = cur.fetchone()
        print(updated)
        conn.commit()
        if not updated:
            raise HTTPException(status_code=404, detail="Patient not found")
        return{"status":"updated", "data":updated}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()

#Delete
@app.delete("/patients")
def delete_patient(patient_id: str):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute("""
            DELETE FROM patients
            WHERE LOWER(patient_id) = LOWER(%s)
            RETURNING *;
        """, (patient_id,))
        deleted = cur.fetchone()
        conn.commit()
        if not deleted:
            raise HTTPException(status_code=404, detail="Patient not found")
        return {"status": "deleted", "data": deleted}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()

#search for a Doctor
@app.get("/doctors")
def search_doctor(
    doctor_id: str = None,
    first_name: str = None,
    specialization: str = None
):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        query = "SELECT * FROM doctors"
        conditions = []
        params = []
        if doctor_id:
            conditions.append("LOWER(doctor_id) = LOWER(%s)")
            params.append(doctor_id)
        if first_name:
            conditions.append("LOWER(first_name) LIKE LOWER(%s)")
            params.append(f"%{first_name}%")
        if specialization:
            conditions.append("LOWER(specialization) LIKE LOWER(%s)")
            params.append(f"%{specialization}%")
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
            print(query)
        cur.execute(query, tuple(params))
        rows = cur.fetchall()
        if not rows:
            raise HTTPException(status_code=404, detail="Doctor not found")
        return {"count": len(rows), "data": rows}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()   

#show all records    
@app.get("/doctors/show all records")
def get_doctors():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM doctors;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return {"data": rows}

#update doctor
@app.put("/doctors")
def update_doctor(doctor_id: str, first_name: str = None, last_name: str=None, specialization: str = None, phone_number: str=None, years_experience: str=None, hospital_branch: str =None, email: str=None):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        updates = []
        params = []
        if first_name:
            updates.append("first_name = %s")
        if last_name:
            updates.append("last_name = %s")
            params.append(last_name)
        if specialization:
            updates.append("specialization = %s")
            params.append(specialization)
        if phone_number:
            updates.append("phone_number = %s")
            params.append(phone_number)
        if years_experience:
            updates.append("years_experience = %s")
            params.append(years_experience)
        if hospital_branch:
            updates.append("hospital_branch = %s")
            params.append(hospital_branch)
        if email:
            updates.append("email =%s")
            params.append(email)
        if not updates:
            raise HTTPException(status_code=400, detail="No fields to update")
        print(updates)
        query = f"""
            UPDATE doctors
            SET {", ".join(updates)}
            WHERE LOWER(doctor_id) = LOWER(%s)
            RETURNING *;
        """
        print(query)
        params.append(doctor_id)
        print(params)
        cur.execute(query, tuple(params))
        updated = cur.fetchone()
        conn.commit()
        if not updated:
            raise HTTPException(status_code=404, detail="Doctor not found")
        return {"status": "updated", "data": updated}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()

#add new appointment
@app.post("/appointments")
def create_appointment(
    patient_id: str,
    doctor_id: str,
    appointment_date: str,
    appointment_time: str,
    reason_for_visit: str
):
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        # if patient exists
        cur.execute(
            "SELECT 1 FROM patients WHERE LOWER(patient_id)=LOWER(%s);",
            (patient_id,)
        )
        if not cur.fetchone():
            raise HTTPException(status_code=404, detail="Patient not found")
        # if doctor exists
        cur.execute(
            "SELECT 1 FROM doctors WHERE LOWER(doctor_id)=LOWER(%s);",
            (doctor_id,)
        )
        if not cur.fetchone():
            raise HTTPException(status_code=404, detail="Doctor not found")
        # doctor availability
        cur.execute("""
            SELECT 1
            FROM appointments
            WHERE LOWER(doctor_id)=LOWER(%s)
              AND appointment_date = %s
              AND appointment_time = %s
              AND status = 'scheduled';
            """, (doctor_id, appointment_date, appointment_time))
        if cur.fetchone():
            raise HTTPException(
                status_code=409,
                detail="Doctor is not available"
            )
        #generate app_id
        cur.execute("""
            SELECT appointment_id
            FROM appointments
            ORDER BY appointment_id DESC
            LIMIT 1;
        """)
        last_appointment = cur.fetchone()
        print(last_appointment)
        if last_appointment:
            last_num = int(last_appointment["appointment_id"][1:])
            appointment_id = f"A{last_num + 1:03d}"
        else:
            appointment_id = "A001"
        # Insert appointment
        query = """
            INSERT INTO appointments (
                appointment_id,
                patient_id,
                doctor_id,
                appointment_date,
                appointment_time,
                reason_for_visit,
                status
            )
            VALUES (%s,%s,%s,%s,%s,%s,'scheduled')
            RETURNING *;
        """
        cur.execute(query, (
            appointment_id,
            patient_id,
            doctor_id,
            appointment_date,
            appointment_time,
            reason_for_visit
        ))
        conn.commit()
        new_appointment = cur.fetchone()
        print(new_appointment)
        cur.close()
        conn.close()
        return {
            "status": "created",
            "data": new_appointment
        }
    except HTTPException as he:
        if conn:
            conn.rollback()
            conn.close()
        raise he
    except Exception as e:
        if conn:
            conn.rollback()
            conn.close()
        raise HTTPException(status_code=500, detail=str(e))

#search apt
@app.get("/appointments")
def search_appointment(appointment_id:str=None, first_name:str=None):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        query = """
            SELECT a.*
            FROM appointments a
            JOIN patients p ON a.patient_id = p.patient_id
            """
        conditions=[]
        params=[]
        if appointment_id:
            conditions.append("LOWER(appointment_id)=LOWER(%s)")
            params.append(appointment_id)
        if first_name:
            conditions.append("LOWER(first_name)=LOWER(%s)")
            params.append(first_name)
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        cur.execute(query, tuple(params))
        rows=cur.fetchall()
        if not rows:
            raise HTTPException(status_code=404, detail="No appointment found")
        return {"count":len(rows), "data":rows}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()

#show all records
@app.get("/appointments")
def get_appointments():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM appointments;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return {"data": rows}

#update apt
@app.put("/appointments")
def update_appointment(
    appointment_id: str,
    first_name: str = None,
    last_name: str = None,
    appointment_date: str = None,
    appointment_time: str = None,
    reason_for_visit: str = None,
    status: str = None
):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try: #if exists
        cur.execute("""
            SELECT * FROM appointments
            WHERE LOWER(appointment_id) = LOWER(%s);
        """, (appointment_id,))
        existing = cur.fetchone()
        print(existing)
        if not existing:
            raise HTTPException(status_code=404, detail="Appointment not found")
        updates = []
        params = []
        if appointment_date:
            updates.append("appointment_date = %s")
            params.append(appointment_date)
        if appointment_time:
            updates.append("appointment_time = %s")
            params.append(appointment_time)
        if reason_for_visit:
            updates.append("reason_for_visit = %s")
            params.append(reason_for_visit)
        if status:
            updates.append("status = %s")
            params.append(status)
        if not updates:
            raise HTTPException(status_code=400, detail="No fields to update")
        print(updates)
        query = f"""
            UPDATE appointments
            SET {", ".join(updates)}
            WHERE LOWER(appointment_id) = LOWER(%s)
            RETURNING *;
        """
        print(query)
        params.append(appointment_id)
        print(params)
        cur.execute(query, tuple(params))
        updated = cur.fetchone()
        conn.commit()
        return {
            "status": "updated",
            "data": updated
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()

#delete apt

#create treatment
@app.post("/treatments")
def create_treatment(
    appointment_id: str,
    treatment_type: str,
    description: str,
    cost: float,
    treatment_date: str,
    payment_method: str = "Pending"
):
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        # Validate appointment exists
        cur.execute("""
            SELECT 
                a.appointment_id,
                a.status,
                p.patient_id,
                d.doctor_id
            FROM appointments a
            JOIN patients p 
                ON a.patient_id = p.patient_id
            JOIN doctors d 
                ON a.doctor_id = d.doctor_id
            WHERE LOWER(a.appointment_id) = LOWER(%s)
        """, (appointment_id,))
        appointment = cur.fetchone()
        if not appointment:
            raise HTTPException(
                status_code=404,
                detail="Appointment not found"
            )
        # Prevent cancelled appointments
        if appointment["status"].lower() == "cancelled":
            raise HTTPException(
                status_code=400,
                detail="Cannot create treatment for cancelled appointment"
            )
        # Generate Treatment ID
        cur.execute("""
            SELECT treatment_id
            FROM treatments
            ORDER BY treatment_id DESC
            LIMIT 1
        """)
        last_treatment = cur.fetchone()
        print(last_treatment)
        if last_treatment:
            last_num = int(last_treatment["treatment_id"][1:])
            new_treatment_id = f"T{last_num + 1:03d}"
        else:
            new_treatment_id = "T001"
        # Insert treatment
        cur.execute("""
            INSERT INTO treatments (
                treatment_id,
                appointment_id,
                treatment_type,
                description,
                cost,
                treatment_date
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING *
        """, (
            new_treatment_id,
            appointment_id,
            treatment_type,
            description,
            cost,
            treatment_date
        ))

        treatment = cur.fetchone()
       # Auto-generate Billing
        cur.execute("""
            SELECT bill_id
            FROM billing
            ORDER BY bill_id DESC
            LIMIT 1
        """)
        last_bill = cur.fetchone()
        if last_bill:
            last_num = int(last_bill["bill_id"][1:])
            new_bill_id = f"B{last_num + 1:03d}"
        else:
            new_bill_id = "B001"
        cur.execute("""
            INSERT INTO billing (
                bill_id,
                patient_id,
                treatment_id,
                bill_date,
                amount,
                payment_method,
                payment_status
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING *
        """, (
            new_bill_id,
            appointment["patient_id"],
            new_treatment_id,
            treatment_date,
            cost,
            payment_method,
            "Pending"
        ))
        billing = cur.fetchone()
        # Update appointment status
        cur.execute("""
            UPDATE appointments
            SET status = 'Completed'
            WHERE LOWER(appointment_id) = LOWER(%s)
        """, (appointment_id,))
        # Commit everything
        conn.commit()
        return {
            "message": "Treatment and billing created successfully",
            "treatment": treatment,
            "billing": billing
        }
    except HTTPException as he:
        if conn:
            conn.rollback()
        raise he
    except Exception as e:
        if conn:
            conn.rollback()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    finally:
        if conn:
            cur.close()
            conn.close()

#show all treatments
@app.get("/treatments")
def get_treatments():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM treatments;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return {"data": rows}

#show all billings
@app.get("/billing")
def get_billing():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM billing;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return {"data": rows}

#search a billing
@app.get("/billing")
def search_billing(bill_id: str = None, patient_id: str = None):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        query = """
            SELECT * FROM billing
        """
        conditions = []
        params = []
        if bill_id:
            conditions.append("LOWER(bill_id) = LOWER(%s)")
            params.append(bill_id)
        if patient_id:
            conditions.append("LOWER(patient_id) = LOWER(%s)")
            params.append(patient_id)
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        cur.execute(query, tuple(params))
        rows = cur.fetchall()
        if not rows:
            raise HTTPException(
                status_code=404,
                detail="No billing records found"
            )
        return {
            "count": len(rows),
            "data": rows
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    finally:
        cur.close()
        conn.close()

#update billing
@app.put("/billing")
def update_billing(
    bill_id: str,
    amount: float = None,
    payment_method: str = None,
    payment_status: str = None
):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:    #check bill exists
        cur.execute("""
            SELECT * FROM billing
            WHERE LOWER(bill_id) = LOWER(%s)
        """, (bill_id,))
        existing = cur.fetchone()
        if not existing:
            raise HTTPException(
                status_code=404,
                detail="Billing not found"
            )
        updates = []
        params = []
        if amount:
            updates.append("amount = %s")
            params.append(amount)
        if payment_method:
            updates.append("payment_method = %s")
            params.append(payment_method)
        if payment_status:
            updates.append("payment_status = %s")
            params.append(payment_status)
        if not updates:
            raise HTTPException(
                status_code=400,
                detail="No fields to update"
            )
        Query = f"""
            UPDATE billing
            SET {", ".join(updates)}
            WHERE LOWER(bill_id) = LOWER(%s)
            RETURNING *
        """
        params.append(bill_id)
        cur.execute(Query, tuple(params))
        updated = cur.fetchone()   
        conn.commit()
        return {
            "status": "updated",
            "data": updated
        }
    except Exception as e:
        conn.rollback()
        raise HTTPException(
            status_code=500,
            detail=str(e)
            )
    finally:
        cur.close()
        conn.close()
   
#sesrch a treatment with bills
@app.get("/treatment")
def search_treatment(treatment_id: str = None, treatment_type: str = None):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        query = """
            SELECT 
                t.treatment_id,
                t.appointment_id,
                t.treatment_type,
                t.description,
                t.cost,
                t.treatment_date,
                b.bill_id,
                b.amount,
                b.payment_method,
                b.payment_status
            FROM treatments t
            LEFT JOIN billing b                         
                ON t.treatment_id = b.treatment_id
        """                                                     ##Treatment always appears, billing is optional
        conditions = []
        params = []
        if treatment_id:
            conditions.append("LOWER(t.treatment_id) = LOWER(%s)")
            params.append(treatment_id)
        if treatment_type:
            conditions.append("LOWER(t.treatment_type) = LOWER(%s)")
            params.append(treatment_type)
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        print(query)
        cur.execute(query, tuple(params))
        rows = cur.fetchall()
        if not rows:
            raise HTTPException(
                status_code=404,
                detail="No treatment records found"
            )
        return {
            "count": len(rows),
            "data": rows
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    finally:
        cur.close()
        conn.close()

# Patient Full History
@app.get("/patients/history")
def patient_history(patient_id: str):
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        query = """
            SELECT 
                p.patient_id,
                p.first_name AS patient_first_name,
                p.last_name  AS patient_last_name,

                a.appointment_date,
                a.reason_for_visit,
                a.status AS appointment_status,

                d.first_name AS doctor_first_name,
                d.last_name  AS doctor_last_name,
                d.specialization,

                t.treatment_type,

                b.amount AS bill_amount,
                b.payment_status

            FROM patients p

            LEFT JOIN appointments a 
                ON p.patient_id = a.patient_id

            LEFT JOIN doctors d 
                ON a.doctor_id = d.doctor_id

            LEFT JOIN treatments t 
                ON a.appointment_id = t.appointment_id

            LEFT JOIN billing b 
                ON t.treatment_id = b.treatment_id

            WHERE LOWER(p.patient_id) = LOWER(%s)

            ORDER BY a.appointment_date DESC;
        """
        cur.execute(query, (patient_id,))
        rows = cur.fetchall()
        if not rows:
            raise HTTPException(
                status_code=404,
                detail=f"No records found for patient_id: {patient_id}"
            )
        return {
            "patient_id": patient_id,
            "total_records": len(rows),
            "data": rows
        }
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Error fetching full patient history"
        )
    finally:
        if conn:
            conn.close()

#Doctor's workload
@app.get("/doctors/workload")
def doctor_workload(doctor_id=str):
    conn = 0
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        query = """
        SELECT 
            d.doctor_id,
            d.first_name,
            COUNT(a.appointment_id) AS total_appointments
        FROM doctors d
        LEFT JOIN appointments a ON d.doctor_id = a.doctor_id
        GROUP BY d.doctor_id, d.first_name
        ORDER BY total_appointments DESC;
        """
        cur.execute(query, (doctor_id,))
        rows = cur.fetchall()
        print(rows)        
        cur.close()
        conn.close()
        if not rows:
            raise HTTPException(
                status_code=404,
                detail=f"No doctor found with ID:{doctor_id}"
            )
        return{
            "doctor_id":doctor_id,
            "record_count":len(rows),
            "data": rows
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        if conn:
            conn.close()
        raise HTTPException(
            status_code=500,
            detail=f"Server error: {str(e)}"
        )

#uvicorn main:app --reload