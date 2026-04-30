# AI Humanizer — Django Version

This is a simple Django conversion of the uploaded React + Express AI Humanizer project.

## Features

- Server-rendered Django UI
- Text humanizer dashboard
- AI detector-style score estimate
- Paraphrase, grammar, summarize, ads, email, essay, product, and social caption tools
- File upload for `.txt`, `.pdf`, and `.docx`
- History stored in SQLite
- Login/signup using Django auth
- Download results as TXT or PDF
- Optional Gemini API support with local fallback processing

## Setup

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

Open: `http://127.0.0.1:8000/`

## Optional Gemini API

Add your key in `.env`:

```env
GEMINI_API_KEY=your_key_here
```

Without a key, the app still runs with local fallback transformations, summarization, and scoring.

## Project structure

```text
ai_humanizer_django/
├── ai_humanizer/      # Django project settings and URLs
├── tools/             # Main Django app
│   ├── templates/     # HTML templates
│   ├── static/        # CSS
│   ├── services.py    # AI/local processing logic
│   ├── models.py      # Generation history
│   └── views.py       # Pages and downloads
├── manage.py
├── requirements.txt
└── README.md
```
