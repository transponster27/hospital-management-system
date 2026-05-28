import os
import pandas as pd
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from groq import Groq
import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# CONFIG
CSV_PATH = "csv_files/hospital_dataset.csv"
VECTOR_PATH = "vector_store"
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# LOAD DOCS
def load_documents():
    df = pd.read_csv(CSV_PATH)

    docs = []
    for _, row in df.iterrows():
        text = f"""
    Patient: {row['Name']}
    Age: {row['Age']}
    Gender: {row['Gender']}
    Blood Type: {row['Blood Type']}
    Condition: {row['Medical Condition']}
    Date of Admission: {row['Date of Admission']}
    Doctor: {row['Doctor']}
    Hospital: {row['Hospital']}
    Insurance Provider: {row['Insurance Provider']}
    Billing: {row['Billing Amount']}
    Room Number: {row['Room Number']}
    Admission Type: {row['Admission Type']}
    Date of Discharge: {row['Discharge Date']}
    Medication: {row['Medication']}
    Test Results: {row['Test Results']}
    """

        docs.append(Document(page_content=text,
                            metadata={"name": row["Name"],
                                    "age": row["Age"],
                                    "gender": row["Gender"],
                                    "blood_type": row["Blood Type"],
                                    "medical_condition": row["Medical Condition"],
                                    "date_of_admission": row["Date of Admission"],
                                    "doctor": row["Doctor"],
                                    "hospital": row["Hospital"],
                                    "insurance_provider": row["Insurance Provider"],
                                    "billing_amount": row["Billing Amount"],
                                    "room_number": row["Room Number"],
                                    "admission_type": row["Admission Type"],
                                    "discharge_date": row["Discharge Date"],
                                    "medication": row["Medication"],
                                    "test_results": row["Test Results"]
                            }
        ))

    return docs

# BUILD DB
def build_db():
    docs = load_documents()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(docs)

    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)

    db = FAISS.from_documents(chunks, embeddings)
    db.save_local("vector_store")
    print(f"Total Docs: {len(docs)}")
    print(f"Total Chunks: {len(chunks)}")
    return db

# LOAD DB SAFE
def load_db():
    if not os.path.exists(VECTOR_PATH):
        return build_db()

    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)

    return FAISS.load_local(
        VECTOR_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

# LLM
def ask_llm(prompt):
    res = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "Use only given hospital context."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=300
    )

    return res.choices[0].message.content

# RAG
def answer_query(db, query):

    results = db.similarity_search_with_score(query, k=5)

    print("\n========== RETRIEVED DOCS ==========\n")

    context_parts = []

    for i, (doc, score) in enumerate(results):

        print(f"RESULT {i+1}")
        print(f"Score: {score}")
        print(doc.page_content)
        print("\n-------------------\n")

        context_parts.append(doc.page_content)

    context = "\n\n".join(context_parts)

    prompt = f"""
    You are a hospital assistant chatbot.

    Answer ONLY using the hospital records below.

    Do not hallucinate or invent information.

    Context:
    {context}

    Question:
    {query}

    Answer:
    """

    answer = ask_llm(prompt)

    return {
        "query": query,
        "response": answer,
        "context_chunks": context_parts
    }

if __name__ == "__main__":
    if not os.path.exists(VECTOR_PATH):
        log.info("Building vector DB...")
        db = build_db()
    else:
        log.info("Loading vector DB...")
        db = load_db()

    while True:
        q = input("\nAsk: ")
        if q == "exit":
            break

        result = answer_query(db, q)

        print("\nANSWER:\n", result["response"])