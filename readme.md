# Hospital Management System
## Overview

The Hospital Management System is a full-stack healthcare operations platform designed to centralize and streamline administrative, analytical, and patient-management workflows within a hospital environment.

The system integrates a FastAPI backend, PostgreSQL relational database, Streamlit frontend dashboard, and an AI-powered retrieval assistant to provide a scalable and interactive healthcare management solution. The platform supports operational workflows such as patient registration, doctor management, appointment scheduling, treatment tracking, billing management, analytics visualization, and natural language querying over hospital records.

The project emphasizes modular backend architecture, structured data validation, relational database design, REST API development, analytics-driven dashboards, and Retrieval-Augmented Generation (RAG) concepts for AI-assisted querying.

## Core Features

### Patient Management
Create, update, search, and delete patient records
Structured patient demographic and medical information handling
Insurance provider tracking
Contact and admission record management
Input validation using Pydantic schemas

### Doctor Management
Doctor profile management
Specialization and department tracking
Doctor workload analysis
Doctor-patient appointment mapping

### Appointment Scheduling
Appointment creation and management
Appointment status tracking
Doctor availability integration
Interactive scheduling workflows
Calendar-based appointment visualization

### Treatment Management
Treatment catalog integration
Treatment assignment and tracking
Automated treatment cost association
Treatment distribution analytics

### Billing & Payment System
Billing record generation
Payment status tracking
Revenue monitoring
Paid vs pending payment analysis
Billing aggregation endpoints

### Dashboard & Analytics
KPI-based operational dashboard
Revenue analytics and visualizations
Appointment insights
Doctor workload tracking
Treatment cost analysis
Payment distribution monitoring
Interactive Plotly visualizations

### AI Chatbot Assistant
Natural language querying over hospital data
Retrieval-Augmented Generation (RAG) pipeline
Semantic similarity search using vector embeddings
Context-aware response generation
AI-assisted operational analytics

#### Technology Stack

Backend:
Python
FastAPI
Pydantic
SQLAlchemy / Psycopg2
REST API architecture

Frontend:
Streamlit
Plotly
Pandas
Streamlit Calendar

Database:
PostgreSQL
Relational schema design
SQL joins and aggregations
Normalized healthcare records

AI & NLP Stack:
LangChain
FAISS Vector Database
Hugging Face Embeddings
all-MiniLM-L6-v2 Embedding Model
Groq API / LLM Integration
Transformers

#### System Architecture

Frontend Layer (Streamlit Dashboard)
            │
            ▼
REST API Layer (FastAPI)
            │
            ▼
Business Logic & Validation
            │
            ▼
PostgreSQL Database
            │
            ▼
Analytics & AI Retrieval Layer

#### AI Chatbot Architecture

The AI assistant is implemented using a Retrieval-Augmented Generation (RAG) workflow to provide context-aware responses based on hospital records.

Workflow:
Hospital CSV records are converted into structured documents
Documents are embedded using sentence-transformer embeddings
Embeddings are stored in a FAISS vector database
User queries are converted into embeddings
Semantic similarity retrieval identifies relevant hospital records
Retrieved context is passed to the LLM
The model generates grounded responses using retrieved context only

#### AI Stack:

Embedding Model: sentence-transformers/all-MiniLM-L6-v2

Vector Database: FAISS

LLM Integration: Groq API with Llama 3.1 models

Frameworks: LangChain, Hugging Face Transformers

#### REST API Functionalities

CRUD Operations:
Patients
Doctors
Appointments
Treatments
Billing

Search & Filtering:
Patient search
Doctor filtering
Appointment filtering
Billing status filtering

Analytics APIs:
Revenue aggregation
Doctor workload metrics
Appointment trends
Treatment distribution

AI Endpoint:
Natural language hospital querying
Semantic retrieval-based responses

#### Data Validation

The project incorporates structured validation mechanisms using Pydantic and backend validation logic.

Validation Features:
Email validation
Contact number validation
Gender validation
Date validation
Payment status validation
Required field enforcement
Error handling and HTTP exception management

#### Database Design

Core Tables:
Patients
Doctors
Appointments
Treatments
Billing
Treatment Catalog

Database Concepts Used:
Primary and foreign keys
Relational joins
Aggregation queries
Transaction management
Data normalization

#### Analytics & Visualization

The dashboard includes interactive analytical visualizations to monitor hospital operations.

Analytical Components:
Revenue tracking
Appointment trends
Treatment analytics
Payment monitoring
Doctor workload visualization
KPI summary cards
Operational distribution charts

Visualization Libraries:
Plotly
Pandas
Streamlit components

## Installation

### Clone Repository
git clone <repository_url>
cd hospital-management-system

### Create Virtual Environment
python -m venv .venv

### Activate Environment
Windows
.venv\Scripts\activate
Linux / macOS
source .venv/bin/activate

### Install Dependencies
pip install -r requirements.txt

## Running the Application
Start Backend Server: uvicorn main:app --reload

Backend URL: http://127.0.0.1:8000

Start Frontend Dashboard: streamlit run app.py

Frontend URL: http://localhost:8501

## Project Structure

hospital-management-system/
│
├── app.py
├── main.py
├── chatbot.py
├── requirements.txt
├── csv_files/
├── vector_store/
├── database/
├── models/
├── routes/
├── schemas/
├── analytics/
└── README.md

### Key Engineering Concepts Demonstrated

#### Backend Engineering
REST API development
Request validation
Error handling
Modular architecture
Service-oriented design
#### Database Engineering
Relational schema modeling
SQL optimization
Aggregation queries
Transaction handling
#### AI Engineering
Retrieval-Augmented Generation (RAG)
Vector embeddings
Semantic similarity search
Context-grounded LLM prompting
#### Frontend Engineering
Interactive dashboards
Data visualization
Real-time API integration
Streamlit UI development

### Future Enhancements
Authentication and authorization
Role-based access control
Cloud deployment
Docker containerization
CI/CD pipelines
OpenAI/GPT integration
Voice-enabled assistant
Predictive healthcare analytics
Doctor recommendation system
Real-time notifications
Multi-user support
Advanced RAG pipelines with hybrid retrieval

### Learning Outcomes

This project demonstrates practical implementation of:

Full-stack application development
Healthcare workflow automation
FastAPI backend engineering
PostgreSQL database integration
Dashboard analytics systems
Retrieval-Augmented Generation (RAG)
Semantic search pipelines
Vector database integration
API-driven frontend communication
Data validation and exception handling
AI-assisted operational querying

## Conclusion

The Hospital Management System combines healthcare administration workflows with modern backend engineering, analytics, and AI-assisted querying capabilities. The project demonstrates integration of relational databases, REST APIs, vector search systems, and large language models into a unified operational platform.

The system is designed to be modular, extensible, and scalable, while also serving as a practical implementation of full-stack software engineering and applied AI concepts in a healthcare operations context.

## Author

Vardah Rehman