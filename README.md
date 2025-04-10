# Resume Classifier

An AI-powered system that automatically analyzes resumes and classifies them into job categories using a fine-tuned DistilBERT model.

## Features

- Multi-format support (PDF, DOCX, TXT)
- Automatic extraction of contact info, skills, and education
- Job category classification with confidence scores
- REST API interface

## Tech Stack

**Backend:** Flask, Hugging Face Transformers, ONNX Runtime, PyPDF2, python-docx

**Frontend:** Next.js, TypeScript, TailwindCSS

**ML Model:** Fine-tuned DistilBERT optimized with ONNX

## Quick Start

### Backend
```bash
cd backend
pip install -r requirements.txt
python app.py
```
Backend runs at http://localhost:5000

### Frontend
```bash
cd frontend
npm install
npm run dev
```
Frontend runs at http://localhost:3000

## API Endpoints

- `GET /health` - Health check
- `POST /api/classify` - Classify a resume
- `GET /api/categories` - List available categories

## Response Format

```json
{
  "classification": {
    "category": "Software Engineer",
    "confidence": 0.87,
    "model_type": "fine-tuned"
  },
  "parsed_data": {
    "email": "user@example.com",
    "skills": ["Python", "React", "Docker"],
    "experience_years": 5
  }
}
```

## License

MIT
