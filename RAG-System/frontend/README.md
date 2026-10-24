# Enterprise RAG Research Report Generator

## Overview

Enterprise RAG Research Report Generator is a full-stack AI-powered application that processes large document collections and automatically generates structured research reports using Retrieval-Augmented Generation (RAG).

The system supports PDF, DOCX, PPTX, and CSV documents, performs semantic search using ChromaDB vector storage, re-ranks retrieved results using FlashRank, and generates high-quality reports using Google Gemini AI.

---

## Features

### Document Processing

* Upload PDF documents
* Upload DOCX documents
* Upload PPTX presentations
* Upload CSV files
* Automatic text extraction
* Automatic chunk generation
* Embedding creation and storage

### Retrieval-Augmented Generation (RAG)

* ChromaDB Vector Database
* Sentence Transformer Embeddings
* Semantic Search
* FlashRank Re-ranking
* Context Retrieval Pipeline

### AI Report Generation

* Google Gemini AI Integration
* Structured Research Reports
* Context-Aware Content Generation

### Export Options

* PDF Export
* DOCX Export
* PPTX Export
* XLSX Export
* HTML Export

### Dashboard Features

* Document Management
* Report History
* Dashboard Statistics
* Document Deletion
* Real-Time Analytics

### Deployment

* Docker Support
* Docker Compose Support

---

## System Architecture

```text
React Frontend
      ↓
Django REST API
      ↓
Retrieval Pipeline
      ↓
ChromaDB Vector Store
      ↓
FlashRank Re-ranking
      ↓
Gemini AI
      ↓
Research Report Generation
```

## Technology Stack

### Frontend

* React.js
* Material UI
* Axios
* React Markdown
* React Icons
* React Router DOM

### Backend

* Django
* Django REST Framework

### AI & NLP

* Google Gemini AI
* Sentence Transformers
* FlashRank

### Vector Database

* ChromaDB

### Database

* SQLite

### DevOps

* Docker
* Docker Compose

---

## API Endpoints

### Documents

```http
POST   /api/documents/upload/
GET    /api/documents/list/
DELETE /api/documents/delete/<document_id>/
POST   /api/documents/query/
```

### Reports

```http
POST /api/reports/generate/
POST /api/reports/download-pdf/
POST /api/reports/download-docx/
POST /api/reports/download-pptx/
POST /api/reports/download-xlsx/
POST /api/reports/download-html/
GET  /api/reports/history/
```

### Dashboard

```http
GET /api/dashboard/stats/
```

---

## Dashboard Example

```json
{
  "documents": 16,
  "chunks": 1199,
  "reports": 4
}
```

---

## Installation

### Backend

```bash
cd backend

pip install -r requirements.txt

python manage.py migrate

python manage.py runserver
```

Backend URL:

```text
http://127.0.0.1:8000
```

### Frontend

```bash
cd frontend

npm install

npm start
```

Frontend URL:

```text
http://localhost:3000
```

---

## Docker Setup

### Build

```bash
docker compose build
```

### Start

```bash
docker compose up
```

### Detached Mode

```bash
docker compose up -d
```

### Stop

```bash
docker compose down
```

---

## Workflow

1. Upload Documents
2. Extract Text
3. Create Chunks
4. Generate Embeddings
5. Store in ChromaDB
6. Retrieve Relevant Chunks
7. Re-rank using FlashRank
8. Generate Report using Gemini AI
9. Export Report

---

## Future Enhancements

* User Authentication
* Multi-user Support
* PostgreSQL Integration
* Cloud Deployment
* Report Templates
* Advanced Analytics
* Chat-Based RAG Interface

---

## Author

Pandiri Sivaramakrishna

Email: [pandirisiva234@gmail.com](mailto:pandirisiva234@gmail.com)

Location: Srikakulam, India

---

## License

This project is developed for educational, research, and portfolio purposes.
