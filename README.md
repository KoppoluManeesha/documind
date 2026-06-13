# DocuMind AI

DocuMind AI is a full-stack AI-powered document analysis platform that enables users to upload PDF documents, extract content, and interact with them through natural language queries. The application leverages Large Language Models (LLMs) to provide intelligent document understanding and information retrieval.

## 🚀 Features

* Upload and analyze PDF documents
* Extract text content from PDFs
* Ask questions about uploaded documents using natural language
* AI-powered document understanding with Llama 3.3 via Groq API
* Metadata extraction using Regex-based processing
* Secure document storage and management
* Responsive user interface
* RESTful API architecture

## 🛠️ Tech Stack

### Frontend

* React.js
* CSS Flexbox

### Backend

* FastAPI
* Python

### Database

* PostgreSQL
* SQLAlchemy ORM

### AI Integration

* Llama 3.3
* Groq API

### Deployment

* Render

## 📂 Project Architecture

Frontend (React.js)
↓
FastAPI Backend
↓
SQLAlchemy ORM
↓
PostgreSQL Database
↓
Groq API (Llama 3.3)

## ⚙️ Installation

### Clone the Repository

```bash
git clone <your-github-repository-url>
cd documind
```

### Backend Setup

```bash
cd backend

python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file inside the backend directory:

```env
DATABASE_URL=your_postgresql_connection_string
GROQ_API_KEY=your_groq_api_key
```

### Run Backend

```bash
uvicorn main:app --reload
```

### Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

## 📸 Application Workflow

1. User uploads a PDF document.
2. Backend extracts text content.
3. Document information is stored in PostgreSQL.
4. User submits a question about the document.
5. Query is sent to Llama 3.3 through Groq API.
6. AI generates a contextual response based on document content.
7. Response is displayed in the user interface.

## 🎯 Key Highlights

* Full-stack application development
* REST API implementation using FastAPI
* Database management with PostgreSQL and SQLAlchemy
* AI-powered document question answering
* Production deployment on Render
* Environment variable management and CORS configuration

## 🔗 Links

### Live Demo

https://documind-frontend-4h76.onrender.com/login

### GitHub Repository

https://github.com/KoppoluManeesha/documind

## 👩‍💻 Author

Koppolu Maneesha

GitHub: https://github.com/KoppoluManeesha

LinkedIn: https://www.linkedin.com/in/koppolu-maneesha-python-developer/
