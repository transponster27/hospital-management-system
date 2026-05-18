#Pydantic validation

from pydantic import BaseModel, EmailStr, field_validator
from datetime import date, datetime
from typing import Optional

class Patient(BaseModel):
    first_name: str
    last_name: str
    gender: str
    date_of_birth: date
    contact_number: str
    address: Optional[str] = None
    insurance_provider: Optional[str] = None
    insurance_number: Optional[str] = None
    email: Optional[EmailStr] = None
    registration_date: date = date.today()

    @field_validator("gender")
    @classmethod
    def validate_gender(cls, v):
        if v.upper() not in ["M", "F"]:
            raise ValueError("Gender must be M or F")
        return v.upper()

    @field_validator("date_of_birth")
    @classmethod
    def validate_dob(cls, v):
        if v > date.today():
            raise ValueError("Date of birth cannot be in the future")
        return v

    @field_validator("contact_number")
    @classmethod
    def validate_contact(cls, v):
        if not v.isdigit() or len(v) < 10:
            raise ValueError("Contact number must be at least 10 digits")
        return v

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        if v and not EmailStr(v):
            raise ValueError("Invalid email address")
        return v

class Appointment(BaseModel):
    patient_id: str
    doctor_id: str
    appointment_date: date
    appointment_time: str
    reason_for_visit: str
    status: str = "scheduled"

    @field_validator("appointment_date")
    @classmethod
    def validate_date(cls, v):
        if v < date.today():
            raise ValueError("Appointment date cannot be in the past")
        return v

class Treatment(BaseModel):
    appointment_id: str
    treatment_type: str
    description: str
    treatment_date: date
    payment_method: Optional[str] = "Cash"

class Billing(BaseModel):
    bill_id: str
    amount: Optional[float] = None
    payment_method: Optional[str] = None
    payment_status: Optional[str] = None

    @field_validator("payment_status")
    @classmethod
    def validate_payment_status(cls, value):
        if value:
            allowed = ["Pending", "Paid", "Cancelled"]
            if value not in allowed:
                raise ValueError(f"Payment status must be one of {allowed}")
        return value
    
    @field_validator("payment_method")
    @classmethod
    def validate_payment_method(cls, value):
        if value:
            allowed = ["Cash", "Credit Card", "Debit Card", "Bank Transfer"]
            if value not in allowed:
                raise ValueError(f"Payment method must be one of {allowed}")
        return value

