# DriveDigest : AI Document Summarizer

An AI-powered document summarization system built with FastAPI, Google Drive API, Gemini AI, and Neon PostgreSQL.

The application automatically connects to a Google Drive folder, downloads supported documents, extracts text, generates AI summaries, and displays them in a modern web dashboard.

---

# Features

- Google OAuth2 Authentication
- Google Drive Folder Integration
- Automatic File Fetching
- PDF Parsing using PyMuPDF
- DOCX Parsing using python-docx
- TXT File Parsing
- AI Summarization using Gemini API
- Neon PostgreSQL Database Integration
- Styled FastAPI + Jinja2 Dashboard
- CSV Report Download
- PDF Report Download
- Summary Modal Viewer
- Automated Document Processing Pipeline
---

# Tech Stack

## Backend
- FastAPI
- SQLAlchemy
- Alembic
- Neon PostgreSQL

## AI
- Google Gemini API

## Google Services
- Google OAuth2
- Google Drive API

## Parsing Libraries
- PyMuPDF
- python-docx

## Frontend
- Jinja2 Templates
- TailwindCSS

---

# System Architecture

```text
Google OAuth Login
        ↓
Google Drive Access
        ↓
Fetch Documents from Drive Folder
        ↓
Download Files
        ↓
Parse PDF / DOCX / TXT
        ↓
Extract Text
        ↓
Send to Gemini API
        ↓
Generate AI Summary
        ↓
Store in Neon PostgreSQL
        ↓
Display in Dashboard
````

---

# Supported File Types

* PDF
* DOCX
* TXT

---

# Project Structure

```text
drive-digest/
│
├── app/
│   ├── core/
│   ├── db/
│   ├── routers/
│   ├── services/
│   ├── templates/
│   └── static/
│
├── screenshots/
├── uploads/
├── drive_downloads/
├── requirements.txt
├── README.md
└── .env
```

---

# Environment Variables

Create a `.env` file:

```env
DATABASE_URL=your_neon_postgres_url

GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REDIRECT_URI=http://localhost:8000/auth

GEMINI_API_KEY=your_gemini_api_key

SESSION_SECRET=your_secret_key
```

---

# Installation

## 1. Clone Repository

```bash
git clone https://github.com/yourusername/drive-digest.git

cd drive-digest
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate:

### Windows

```bash
venv\Scripts\activate
```

### Mac/Linux

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Run Server

```bash
uvicorn app.main:app --reload
```

---

# Google OAuth Setup

## Enable APIs

Enable:

* Google Drive API
* Google OAuth Consent Screen

## Add Test Users

Add your Gmail inside:

```text
OAuth Consent Screen → Audience → Test Users
```

---

# How It Works

1. User logs in with Google
2. Application accesses configured Drive folder
3. Files are downloaded automatically
4. Text is extracted from documents
5. Gemini AI generates summaries
6. Summaries are stored in Neon PostgreSQL
7. Dashboard displays generated summaries

---

# Screenshots

## Landing Page
Before Login:

![Landing Page](screenshots/Screenshot%202026-06-06%20221517.png)

After Login:
![](screenshots/Screenshot%202026-06-06%20221342.png)

---


## Summary Modal

![Summary Modal](screenshots/Screenshot%202026-06-06%20215928.png)
![](screenshots/Screenshot%202026-06-06%20220243.png)

---
## Download(Pdf and csv)
![](screenshots/Screenshot%202026-06-06%20220504.png)
![pdf](screenshots/Screenshot%202026-06-06%20220643.png)
![csv](screenshots/Screenshot%202026-06-06%20220854.png)

## Terminal Logs

![Terminal Logs](screenshots/Screenshot%202026-06-06%20221037.png)
![](screenshots/Screenshot%202026-06-06%20221202.png)
![](screenshots/Screenshot%202026-06-06%20221250.png)


---

# AI Summarization Example

## Input

PDF Resume / Research Paper / Technical Document

## Output

* File Name
* 5–10 sentence AI-generated summary
* Downloadable reports

---

# API Routes

| Route                   | Description                 |
| ----------------------- | --------------------------- |
| `/`                     | Landing Page                |
| `/login`                | Google OAuth Login          |
| `/logout`               | Logout User                 |
| `/documents`            | View Summaries              |
| `/process-drive-folder` | Fetch & Process Drive Files |
| `/download/csv`         | Download CSV Report         |
| `/download/pdf`         | Download PDF Report         |

---

# Database

The project uses Neon PostgreSQL for storing:

* Document metadata
* Extracted text
* Generated summaries


---

# Future Improvements(If I have to work further...)

* Async background processing
* Celery task queue
* Better chunking for large PDFs
* Real-time progress updates
* Multi-folder support
* Search and filtering
* Docker deployment

---

# Author

Asmita Mallick