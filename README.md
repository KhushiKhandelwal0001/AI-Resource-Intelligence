# 🤖 AI Resource Intelligence

### AI-Powered Document Analysis, Intelligence & Semantic Search Platform

**AI Resource Intelligence** is a Flask-based AI application that transforms uploaded documents into structured, actionable intelligence.

The platform can process **CVs / Resumes, Annual Reports, Research Papers, Job Descriptions, and other business documents**, extract meaningful information, generate document-specific insights, identify technical skills where applicable, provide career intelligence for resumes, and enable intelligent search across uploaded documents.

---

## 🌟 Project Overview

Traditional document analysis often requires manually reading large documents to find important information.

AI Resource Intelligence simplifies this process by combining:

* 📄 Document Processing
* 🧠 AI-Based Analysis
* 🔍 Semantic Search
* 📊 Document Analytics
* 🛠️ Skill Extraction
* 💼 Career Intelligence
* 🤖 Resource Intelligence Agent
* 📚 Retrieval-Augmented Generation (RAG)
* ⚡ Flask REST APIs

The goal is to turn unstructured documents into **searchable, structured and actionable intelligence**.

---

## ✨ Key Features

### 📄 Multi-Format Document Processing

Upload and process:

* PDF
* DOCX
* TXT

The platform extracts text and document metadata automatically.

---

### 🧠 Intelligent Document Analysis

The system identifies the type of uploaded document and performs analysis according to its context.

Supported document categories include:

* CV / Resume
* Annual Report
* Research Paper
* Job Description
* Policy Document
* General Business Document

This allows the platform to avoid applying the same analysis logic to every document.

---

### 📋 Document Information

The platform extracts important document-level information such as:

* File name
* File type
* Document type
* Number of pages
* Word count
* Character count
* Email information
* Phone information
* LinkedIn information

---

### 📝 AI Document Summary

The platform generates a structured summary based on the uploaded document.

The analysis is designed to be **document-aware**, meaning that a CV, Annual Report, Research Paper and Job Description can be interpreted differently.

---

### 🔑 Key Information Extraction

Important information is extracted from the document and presented in a structured format.

For CV / Resume documents, this can include:

* Education
* Experience
* Projects
* Certifications
* Skills

For business and research documents, the platform focuses on document-relevant information.

---

### 🛠️ Technical Skill Extraction

For CV / Resume documents, the system identifies technical skills across areas such as:

* Python
* SQL
* Data Analytics
* Data Visualization
* Statistics
* Machine Learning
* Artificial Intelligence
* Generative AI
* NLP
* Databases
* Development
* Document AI
* Agentic AI

Skills are presented individually so they can be easily interpreted.

---

### 📊 AI Insights

The platform generates insights from the uploaded resource.

Examples include:

* Technical capability analysis
* AI / ML exposure
* Data analytics exposure
* Development capabilities
* Document intelligence capabilities
* Career-oriented observations

Insights are adapted according to the type of document being analyzed.

---

### 💼 Career Intelligence

Career intelligence is primarily available for **CV / Resume documents**.

The system can identify potential career directions based on the skills and information detected in the document.

Example career areas include:

* Data Analyst
* Data Scientist
* Machine Learning Engineer
* AI / ML Engineer
* Generative AI Engineer
* AI / RAG Engineer

---

## 🔎 Resource Intelligence Assistant

The platform includes an **AI Research & Knowledge Assistant** that allows users to ask questions about an uploaded document.

Example questions:

```text
What skills are mentioned in this CV?

What projects are included in the document?

What is this document about?

What experience is mentioned?

Find information about FICCI.
```

The assistant uses document retrieval to locate relevant information.

---

## 📚 Retrieval-Augmented Generation (RAG)

The application includes a local RAG architecture for document intelligence.

### RAG Pipeline

```text
Uploaded Document
        ↓
Text Extraction
        ↓
Document Processing
        ↓
Text Chunking
        ↓
Sentence Embeddings
        ↓
Vector Representation
        ↓
Semantic Retrieval
        ↓
Resource Intelligence Agent
        ↓
Relevant Answer
```

The project uses:

```text
SentenceTransformer
all-MiniLM-L6-v2
```

for semantic document representation.

---

## 🔍 Intelligent Search

The search system combines:

### Exact Keyword Search

Useful for targeted searches such as:

```text
FICCI
Machine Learning
Python
Annual Report
```

### Semantic Search

Useful for conceptual questions such as:

```text
What are the major business areas discussed in this report?
```

The goal is to return focused information for direct keyword searches while retaining semantic retrieval for broader questions.

---

## 🤖 Resource Intelligence Agent

The project contains a dedicated Resource Intelligence Agent responsible for document-based question answering.

```text
User Question
      ↓
Resource Intelligence Agent
      ↓
Exact Keyword Search
      ↓
Semantic Retrieval
      ↓
Relevant Document Context
      ↓
Answer
```

This architecture allows the system to combine deterministic retrieval with semantic intelligence.

---

## 🏗️ Project Architecture

```text
AI-Resource-Intelligence
│
├── agents/
│   ├── __init__.py
│   ├── agent_controller.py
│   └── resource_agent.py
│
├── document_processing/
│   ├── __init__.py
│   └── document_processor.py
│
├── rag/
│   ├── __init__.py
│   └── retriever.py
│
├── data/
│   ├── uploads/
│   ├── processed/
│   └── embeddings/
│
├── reports/
│
├── templates/
│   └── index.html
│
├── static/
│   ├── style.css
│   └── script.js
│
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🧩 System Architecture

```text
                    ┌─────────────────────┐
                    │      User           │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Flask Web UI      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Document Upload     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Document Processor  │
                    └──────────┬──────────┘
                               │
                ┌──────────────┼──────────────┐
                ▼              ▼              ▼
        ┌────────────┐ ┌────────────┐ ┌────────────┐
        │ Document   │ │ AI Analysis│ │ Skill      │
        │ Information│ │ & Insights │ │ Extraction │
        └────────────┘ └────────────┘ └────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      RAG Layer      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Resource Intelligence│
                    │       Agent         │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Intelligent Results │
                    └─────────────────────┘
```

---

## 🛠️ Technology Stack

### Backend

* Python
* Flask
* Flask-CORS

### Document Processing

* PyMuPDF
* python-docx
* Regular Expressions

### Data & Analytics

* Pandas
* NumPy
* Scikit-learn

### AI / NLP

* Sentence Transformers
* Transformers
* PyTorch
* Semantic Embeddings

### Frontend

* HTML5
* CSS3
* JavaScript

### Version Control

* Git
* GitHub

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/KhushiKhandelwal0001/AI-Resource-Intelligence.git
```

Move into the project:

```bash
cd AI-Resource-Intelligence
```

---

### 2. Create a virtual environment

Windows:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

---

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

---

### 4. Run the application

```powershell
python app.py
```

The application will be available at:

```text
http://127.0.0.1:5001
```

---

## ❤️ Health Check

The application provides a health endpoint:

```text
http://127.0.0.1:5001/api/health
```

Example response:

```json
{
  "status": "online",
  "application": "AI Resource Intelligence Platform",
  "version": "1.0.0"
}
```

---

## 🔌 API Endpoints

### Home

```text
GET /
```

### Resource Intelligence

```text
GET /resource-intelligence
```

### Health Check

```text
GET /api/health
```

### Document Upload

```text
POST /api/upload
```

### AI Search

```text
POST /api/search
```

---

## 📤 Supported Files

| File Type | Supported |
| --------- | --------- |
| PDF       | ✅         |
| DOCX      | ✅         |
| TXT       | ✅         |

Maximum upload size:

```text
25 MB
```

---

## 🔐 Data & Git Security

Uploaded resources and generated embeddings are intentionally excluded from Git using `.gitignore`.

Excluded directories include:

```text
data/uploads/
data/processed/
data/embeddings/
```

Virtual environments are also excluded:

```text
.venv/
venv/
```

This prevents potentially sensitive documents and large generated files from being committed to the repository.

---

## 🚀 Future Enhancements

The platform is designed to evolve into a larger AI-powered intelligence system.

Planned enhancements include:

* 🤖 Advanced Generative AI integration
* 📑 Automated professional report generation
* 📊 Advanced document analytics
* 💼 Job Description vs CV matching
* 🎯 Skill-gap analysis
* 🧠 Advanced agent orchestration
* 📚 Multi-document RAG
* 🔎 Improved document search
* 📈 Career recommendation engine
* 📄 AI-generated PDF reports
* 📊 AI-generated presentation reports
* 🔗 FICCI intelligence integration
* ⚡ Production deployment
* 🔐 Authentication and user management

---

## 🎯 Project Objective

The long-term objective of **AI Resource Intelligence** is to create an intelligent document platform capable of converting unstructured resources into:

```text
Documents
    ↓
Information
    ↓
Knowledge
    ↓
Insights
    ↓
Intelligence
    ↓
Actionable Decisions
```

The project combines **Document AI, NLP, Semantic Search, RAG, Analytics and Agentic AI concepts** into a single practical application.

---

## 👩‍💻 Author

### Khushi Khandelwal

**BBA | Data Analytics | Data Science | AI/ML**

Interested in:

* Data Analytics
* Data Science
* Artificial Intelligence
* Machine Learning
* Generative AI
* RAG Systems
* Agentic AI
* Business Intelligence

---

## ⭐ GitHub

If you find this project useful, consider giving it a ⭐ on GitHub.

**Repository:**
https://github.com/KhushiKhandelwal0001/AI-Resource-Intelligence

---

## 📌 Project Status

**Version:** `1.0.0`

**Status:** 🟢 Active Development

This project is continuously being improved with new AI, analytics, document intelligence and agent-based capabilities.
