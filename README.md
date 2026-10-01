# AI-Powered Ambient Scribe & Evidence-Based Clinical Assistant

An AI-powered healthcare assistant that combines **ambient clinical documentation** with **evidence-based clinical question answering**.

The system converts doctor-patient conversations into structured SOAP notes and provides evidence-grounded answers to clinical queries using medical literature and retrieved sources.

---

## Overview

The project provides two primary workflows:

### 1. Ambient Clinical Documentation

Doctor-Patient Conversation → Speech-to-Text → Privacy Protection → Clinical Extraction → SOAP Generation → Verification → Clinician Review

### 2. Evidence-Based Clinical Q&A

Clinical Question → Query Understanding → Medical Literature Retrieval → Evidence Generation → Safety Validation → Cited Answer

The system follows a **human-in-the-loop approach**, where generated clinical outputs can be reviewed and approved by a clinician.

---

## Key Features

- 🎙️ Live microphone recording
- 📁 Audio file upload
- 📝 Automatic speech-to-text transcription
- 🔐 PHI detection and redaction
- 🧠 Clinical entity extraction
- 📋 AI-generated SOAP notes
- ✅ SOAP verification and completeness checks
- 🔎 Clinical knowledge search
- 📚 Evidence-based medical answers
- 🔗 Source citations
- 🤖 LangGraph-based agentic workflow
- 🛡️ Healthcare safety guardrails
- 👨‍⚕️ Human-in-the-loop clinical review
- 💻 Streamlit clinical interface
- 🗄️ PostgreSQL persistence
- 🔍 Vector-based medical literature retrieval

---

# System Architecture

```text
                         ┌──────────────────────────┐
                         │      Streamlit UI        │
                         │     Clinician Portal     │
                         └────────────┬─────────────┘
                                      │
                         ┌────────────▼─────────────┐
                         │         FastAPI          │
                         │        API Layer         │
                         └────────────┬─────────────┘
                                      │
                         ┌────────────▼─────────────┐
                         │        LangGraph         │
                         │    Agent Orchestration   │
                         └────────────┬─────────────┘
                                      │
                ┌─────────────────────┴─────────────────────┐
                │                                           │
       ┌────────▼────────┐                         ┌────────▼────────┐
       │ Ambient Scribe  │                         │ Clinical Q&A    │
       │    Workflow    │                         │    Workflow     │
       └────────┬────────┘                         └────────┬────────┘
                │                                           │
       ┌────────▼────────┐                         ┌────────▼────────┐
       │ Whisper ASR     │                         │ Qdrant Vector   │
       │ Speech-to-Text  │                         │ Database        │
       └────────┬────────┘                         └────────┬────────┘
                │                                           │
       ┌────────▼────────┐                         ┌────────▼────────┐
       │ Privacy / PHI   │                         │ Medical         │
       │ Protection      │                         │ Literature      │
       └────────┬────────┘                         └────────┬────────┘
                │                                           │
       ┌────────▼────────┐                         ┌────────▼────────┐
       │ Clinical        │                         │ Qwen2.5 3B      │
       │ Extraction      │                         │ LLM             │
       └────────┬────────┘                         └────────┬────────┘
                │                                           │
       ┌────────▼────────┐                         ┌────────▼────────┐
       │ SOAP Generator  │                         │ Safety +        │
       │      LLM        │                         │ Citations       │
       └────────┬────────┘                         └─────────────────┘
                │
       ┌────────▼────────┐
       │ Verification    │
       │ Agent           │
       └─────────────────┘
Workflow A — Ambient Clinical Documentation
Doctor-Patient Conversation
            │
            ▼
        Audio Input
       ┌────┴────┐
       │         │
 Microphone   Audio Upload
       │         │
       └────┬────┘
            ▼
       Whisper ASR
            │
            ▼
      Raw Transcript
            │
            ▼
     Privacy / PHI Agent
            │
            ▼
    Redacted Transcript
            │
            ▼
 Clinical Extraction Agent
            │
            ▼
 Structured Clinical Entities
            │
            ▼
       SOAP Generator
            │
            ▼
         SOAP Draft
            │
            ▼
     Verification Agent
            │
            ▼
       Verified SOAP
            │
            ▼
      Clinician Review
Output
Redacted transcript
Clinical entities
Structured SOAP note
Verification result
Clinician-editable output
Workflow B — Evidence-Based Clinical Q&A
Clinical Question
        │
        ▼
  Query Understanding
        │
        ▼
Intent & Entity Extraction
        │
        ▼
Medical Literature Retrieval
        │
        ▼
      Qdrant
        │
        ▼
 Relevant Evidence Chunks
        │
        ▼
     Qwen2.5 3B
        │
        ▼
 Evidence-Based Answer
        │
        ▼
    Safety Validation
        │
        ▼
   Citation Verification
        │
        ▼
  Clinician-Ready Answer
Agentic Workflow

The system uses LangGraph to orchestrate specialized agents.

Ambient Scribe
Audio Agent
     ↓
Privacy Agent
     ↓
Clinical Extraction Agent
     ↓
SOAP Agent
     ↓
Verification Agent
Clinical Q&A
Query Agent
     ↓
Retrieval Agent
     ↓
Evidence Agent
     ↓
Safety Agent
     ↓
Response Agent

Each agent performs a specific task while sharing structured state through the LangGraph workflow.

Technology Stack
Category	Technology
Programming Language	Python
Frontend	Streamlit
Backend	FastAPI
Speech-to-Text	OpenAI Whisper
LLM	Qwen2.5 3B
Local LLM Runtime	Ollama
Agent Orchestration	LangGraph
LLM Framework	LangChain
Vector Database	Qdrant
Database	PostgreSQL
Medical Literature	PubMed / Medical Sources
Evaluation	RAGAS
AI Models
Speech Recognition

OpenAI Whisper

Used to convert consultation audio into clinical transcripts.

Audio → Whisper → Transcript
Language Model

Qwen2.5 3B

Used for:

SOAP note generation
Evidence-based response generation
Structured clinical output
Clinical context processing

The model can be executed locally using Ollama.

RAG Pipeline

The Clinical Knowledge workflow uses Retrieval-Augmented Generation.

Clinical Query
      │
      ▼
Query Processing
      │
      ▼
Embedding
      │
      ▼
Qdrant Search
      │
      ▼
Relevant Medical Documents
      │
      ▼
Context Construction
      │
      ▼
Qwen2.5 3B
      │
      ▼
Evidence-Grounded Answer
      │
      ▼
Citations
Privacy & Safety

The system follows a privacy-first and human-in-the-loop approach.

Privacy
PHI detection
PHI redaction
Privacy-protected transcripts
Reduced exposure of patient identifiers
Safety
Evidence-grounded responses
Safety validation
Hallucination checks
Source citations
Clinician review
No autonomous diagnosis or treatment decisions

This project is designed as clinical decision support and documentation assistance, not as a replacement for qualified healthcare professionals.

Frontend

The Streamlit application provides two primary workflows.

Clinical Documentation
Upload Audio
     OR
Record Using Microphone
     ↓
Process Consultation
     ↓
Transcript
     ↓
Redacted Transcript
     ↓
SOAP Note
     ↓
Review / Edit
Clinical Knowledge
Enter Clinical Question
        ↓
Search Evidence
        ↓
Retrieve Medical Literature
        ↓
Generate Answer
        ↓
Display Citations
Example — Ambient Scribe
Input

"I have been having fever and cold. Please suggest what I should do."

Redacted Transcript

I have been having fever and cold. Please suggest what I should do.

Generated SOAP Note

SUBJECTIVE

Patient reports fever and cold symptoms.
Duration not specified.
No additional symptoms provided.

OBJECTIVE

Vital signs not available.
Physical examination not available.
Investigations not available.

ASSESSMENT

Fever with upper respiratory symptoms.
Cause cannot be determined from the available information.

PLAN

Rest and adequate fluid intake.
Further clinical assessment if symptoms persist or worsen.
Seek urgent medical attention for difficulty breathing or other severe symptoms.
Example — Clinical Knowledge
Question

What are the common symptoms of influenza?

Evidence-Based Answer

Common symptoms may include:

Fever or chills
Cough
Sore throat
Runny or stuffy nose
Headache
Muscle or body aches
Fatigue

The system provides supporting medical sources along with the generated answer.

Project Structure
TCS/
│
├── audio/
│   ├── transcriber.py
│   └── test_transcriber.py
│
├── llm/
│   ├── soap_generator.py
│   └── test_soap_generator.py
│
├── backend/
│   ├── api/
│   ├── core/
│   └── main.py
│
├── frontend/
│   └── app.py
│
├── data/
│   └── medical_documents/
│
├── tests/
│
├── requirements.txt
├── .env
├── .gitignore
└── README.md
Installation
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd TCS

Create a virtual environment:

python -m venv venv

Activate it on Windows:

venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt
Environment Variables

Create a .env file and add the required configuration:

OPENAI_API_KEY=your_api_key
DATABASE_URL=your_database_url
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_key

Do not commit .env or API keys to GitHub.

Running the Backend
uvicorn backend.main:app --reload

Backend:

http://127.0.0.1:8000
Running the Frontend
streamlit run app.py

The Streamlit application will open in the browser.

Future Scope
HL7 / FHIR integration
EHR integration
Additional medical literature sources
Multilingual clinical transcription
Speaker diarization
Advanced clinical entity extraction
Improved hallucination detection
Automated evaluation pipelines
Role-based authentication
Advanced audit trails
Scalable cloud deployment
Enhanced clinical safety guardrails
