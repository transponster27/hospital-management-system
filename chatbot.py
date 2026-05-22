import pandas as pd
from langchain.schema import Document
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load dataset
df = pd.read_csv("csv_files/hospital_dataset.csv")

# Convert rows into readable documents
documents = []

for _, row in df.iterrows():

    text = f"""
    Patient Name: {row['Name']}
    Age: {row['Age']}
    Gender: {row['Gender']}
    Blood Type: {row['Blood Type']}
    Medical Condition: {row['Medical Condition']}
    Doctor: {row['Doctor']}
    Hospital: {row['Hospital']}
    Admission Type: {row['Admission Type']}
    Medication: {row['Medication']}
    Test Results: {row['Test Results']}
    Billing Amount: {row['Billing Amount']}
    """
    documents.append(
        Document(page_content=text)
    )

# Split text
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

docs = splitter.split_documents(documents)

# Embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Create FAISS vector DB
vector_db = FAISS.from_documents(
    docs,
    embeddings
)

# Save locally
vector_db.save_local("vector_store")

print("Vector DB created successfully")