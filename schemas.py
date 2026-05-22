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

    # @field_validator("first_name", "last_name")
    # @classmethod
    # def validate_name(cls, v):
    #     if not v.isalpha():
    #         raise ValueError("Field cannot be empty")
    #     if len(v) < 2:
    #         raise ValueError("Name must be at least 2 characters long")
    #     return v.title()
        
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

    # @field_validator("contact_number")
    # @classmethod
    # def validate_contact(cls, v):
    #     if not v.strip():
    #         raise ValueError("Contact number required")
    #     if not v.isdigit() or len(v) < 10:
    #         raise ValueError("Contact number must be at least 10 digits")
    #     return v

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        if v and not EmailStr():
            raise ValueError("Invalid email address")
        return v

class Appointment(BaseModel):
    patient_id: str
    doctor_id: str
    appointment_date: date
    appointment_time: str
    reason_for_visit: str
    status: str = "scheduled"

    # @field_validator(
    #     "patient_id",
    #     "doctor_id",
    #     "reason_for_visit"
    # )
    # @classmethod
    # def validate_required(cls, v):

    #     if not v.strip():
    #         raise ValueError("Field cannot be empty")
    #     return v

    @field_validator("appointment_date")
    @classmethod
    def validate_date(cls, v):
        if v < date.today():
            raise ValueError("Appointment date cannot be in the past")
        return v

    @field_validator("status")
    @classmethod
    def validate_status(cls, v):

        allowed = [
            "scheduled",
            "completed",
            "cancelled"
        ]

        if v.lower() not in allowed:
            raise ValueError(
                f"Status must be one of {allowed}"
            )

        return v.lower()

class Treatment(BaseModel):
    appointment_id: str
    treatment_type: str
    description: str
    treatment_date: date
    payment_method: Optional[str] = "Cash"

    # @field_validator(
    #     "appointment_id",
    #     "treatment_type",
    #     "description"
    # )
    # @classmethod
    # def validate(cls,v):
    #     if not v.strip():
    #         raise ValueError("Field cannot be empty")
    #     return v

    @field_validator("payment_method")
    @classmethod
    def validate_payment_method(cls, value):

        allowed = [
            "Cash",
            "Credit Card",
            "Debit Card",
            "Bank Transfer"
        ]

        if value not in allowed:
            raise ValueError(
                f"Payment method must be one of {allowed}"
            )

        return value

class Billing(BaseModel):
    bill_id: str
    amount: Optional[float] = None
    payment_method: Optional[str] = None
    payment_status: Optional[str] = None

    @field_validator("bill_id")
    @classmethod
    def validate_bill_id(cls, value):
        if not value.strip():
            raise ValueError("Bill ID cannot be empty")
        return value

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, value):
        if value < 0:
            raise ValueError("Amount cannot be negative")
        return value

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

class ChatRequest(BaseModel):
    query: str
