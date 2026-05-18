CREATE TABLE IF NOT EXISTS patients (
    patient_id TEXT PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    gender TEXT,
    date_of_birth DATE,
    contact_number TEXT,
    address TEXT,
    registration_date DATE,
    insurance_provider TEXT,
    insurance_number TEXT,
    email TEXT
);

CREATE TABLE IF NOT EXISTS doctors (
    doctor_id TEXT PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    specialization TEXT NOT NULL,
    phone_number TEXT,
    years_experience TEXT,
    hospital_branch TEXT,
    email TEXT
);

CREATE TABLE IF NOT EXISTS appointments (
    appointment_id TEXT PRIMARY KEY,
    patient_id TEXT NOT NULL,
    doctor_id TEXT NOT NULL,
    appointment_date DATE,
    appointment_time TIME,
    reason_for_visit TEXT,
    status TEXT,

    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS treatments (
    treatment_id TEXT PRIMARY KEY,
    appointment_id TEXT NOT NULL,
    treatment_type TEXT,
    description TEXT,
    cost DECIMAL(10,2),
    treatment_date DATE,

    FOREIGN KEY (appointment_id) REFERENCES appointments(appointment_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS billing (
    bill_id TEXT PRIMARY KEY,
    patient_id TEXT NOT NULL,
    treatment_id TEXT NOT NULL,
    bill_date DATE,
    amount DECIMAL(10,2),
    payment_method TEXT,
    payment_status TEXT,

    FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE,
    FOREIGN KEY (treatment_id) REFERENCES treatments(treatment_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS treatment_catalog (
    catalog_id SERIAL PRIMARY KEY,
    treatment_type VARCHAR(100),
    description VARCHAR(100),
    cost NUMERIC(10,2)

    FOREIGN KEY (treatment_type) REFERENCES treatments(treatment_type) ON DELETE CASCADE
    FOREIGN KEY (description) REFERENCES treatments(description) ON DELETE CASCADE
    FOREIGN KEY (cost) REFERENCES treatments(cost) ON DELETE CASCADE
);