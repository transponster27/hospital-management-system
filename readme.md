# Hospital Management System

## Overview

This project is a full-stack Hospital Management System designed to streamline healthcare administration workflows including patient management, doctor records, appointment scheduling, treatments, billing, analytics, and AI-assisted querying.

The platform combines a FastAPI backend, PostgreSQL database, and Streamlit frontend dashboard to provide an interactive and scalable healthcare operations environment with real-time analytics and visualization capabilities.

---

## Features

### Patient Management
- Add, update, search, and delete patient records
- Input validation using Pydantic
- Insurance and contact management
- Patient history tracking

### Doctor Management
- Search and update doctor information
- Doctor workload analytics
- Specialization tracking

### Appointment System
- Appointment creation and scheduling
- Interactive appointment calendar
- Appointment status tracking
- Doctor-patient mapping

### Treatment Management
- Treatment catalog integration
- Automated treatment cost retrieval
- Treatment analytics and visualization
- Billing automation linked to treatments

### Billing System
- Billing generation and updates
- Payment tracking
- Revenue analytics
- Pending and paid payment monitoring

### Dashboard & Analytics
- KPI metric cards
- Revenue tracking
- Appointment heatmaps
- Doctor workload visualizations
- Treatment cost analytics
- Payment distribution charts
- Interactive Plotly visualizations

### AI Chatbot Assistant
- Natural language hospital queries
- Real-time SQL-backed responses
- Operational analytics assistant
- Rule-based NLP implementation

---

## Tech Stack

### Backend
- FastAPI
- Python
- PostgreSQL
- Psycopg2
- Pydantic

### Frontend
- Streamlit
- Plotly
- Pandas
- Streamlit Calendar

### Database
- PostgreSQL Relational Database
- SQL Queries & Joins
- Automated ID Generation

---

## System Architecture

Frontend (Streamlit Dashboard)
↓
REST API Layer (FastAPI)
↓
Business Logic & Validation
↓
PostgreSQL Database
↓
Analytics & AI Assistant

---

## Key Functionalities

### REST APIs
- CRUD operations for all hospital entities
- Search and filtering endpoints
- Aggregation and analytics endpoints
- AI chatbot endpoint

### Data Validation
- Email validation
- Contact number validation
- Date validation
- Payment status validation
- Gender validation

### Analytics
- Revenue trends
- Treatment distribution
- Appointment analytics
- Billing status insights
- Doctor workload tracking

---

## AI Chatbot Workflow

1. User submits a natural language query
2. Frontend sends request to chatbot API
3. Backend identifies intent using keyword mapping
4. SQL queries execute against hospital database
5. Structured response is returned to frontend
6. Real-time insights displayed to user

---

## Installation

### Clone Repository

```bash
git clone <repository_url>
cd hospital-management-system
```

### Create Virtual Environment
python -m venv .venv

#### Activate Environment
Windows
.venv\Scripts\activate
Linux/Mac
source .venv/bin/activate

### Install Dependencies
pip install -r requirements.txt

### Run Backend
uvicorn main:app --reload

#### Backend runs on:

http://127.0.0.1:8000

### Run Frontend
streamlit run app.py

#### Frontend runs on:

http://localhost:8501
---

## Database Tables
Patients
Doctors
Appointments
Treatments
Billing
Treatment Catalog
---

## Future Enhancements
OpenAI/GPT integration
RAG-based hospital knowledge assistant
Voice-enabled chatbot
Predictive patient analytics
Doctor recommendation system
Authentication & role-based access
Cloud deployment
Docker containerization
CI/CD pipelines
Real-time notifications
Learning Outcomes

##  Conclusion

This project demonstrates:
Full-stack application development
API design and integration
Database normalization
Healthcare workflow automation
Dashboard analytics
AI-assisted querying systems
Data validation and error handling
Interactive UI development


## Author
Vardah Rehman