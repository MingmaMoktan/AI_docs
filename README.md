# AI Docs — MVP

Django app to generate documentation from code/sql zips.

## Run locally (WSL)
1. python3 -m venv venv
2. source venv/bin/activate
3. pip install -r requirements.txt
4. export DJANGO_SECRET_KEY="change-me"
5. python manage.py migrate
6. python manage.py runserver



ai_docs/
├── ai_docs/                # Main Django project folder
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── core/                   # Main app (handles uploads, parsing, LLM calls, docs)
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py           # ProjectUpload, GeneratedDoc
│   ├── views.py            # upload, parse, generate_docs
│   ├── forms.py            # Upload form
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── parser.py       # SQL/Python/YAML parsing
│   │   ├── zip_handler.py  # extract ZIPs + folder walker
│   │   ├── formatter.py    # Clean Markdown or HTML formatting
│   │   └── file_utils.py   # file type detection, safe paths
│   ├── llm/
│   │   ├── __init__.py
│   │   └── generator.py    # OpenAI/Groq LLM interface
│   ├── templates/
│   │   ├── base.html
│   │   ├── upload.html
│   │   ├── docs_generated.html
│   │   ├── login.html
│   │   ├── register.html
│   │   └── dashboard.html
│   ├── urls.py
│   └── static/
│       ├── css/
│       ├── js/
│       └── img/
│
├── media/                  # Uploaded ZIPs (user uploads)
│
├── venv/                   # Virtual environment
│
├── requirements.txt
├── manage.py
├── .gitignore
├── .env
└── README.md
ai_docs/
├── ai_docs/                # Main Django project folder
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── core/                   # Main app (handles uploads, parsing, LLM calls, docs)
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py           # ProjectUpload, GeneratedDoc
│   ├── views.py            # upload, parse, generate_docs
│   ├── forms.py            # Upload form
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── parser.py       # SQL/Python/YAML parsing
│   │   ├── zip_handler.py  # extract ZIPs + folder walker
│   │   ├── formatter.py    # Clean Markdown or HTML formatting
│   │   └── file_utils.py   # file type detection, safe paths
│   ├── llm/
│   │   ├── __init__.py
│   │   └── generator.py    # OpenAI/Groq LLM interface
│   ├── templates/
│   │   ├── base.html
│   │   ├── upload.html
│   │   ├── docs_generated.html
│   │   ├── login.html
│   │   ├── register.html
│   │   └── dashboard.html
│   ├── urls.py
│   └── static/
│       ├── css/
│       ├── js/
│       └── img/
│
├── media/                  # Uploaded ZIPs (user uploads)
│
├── venv/                   # Virtual environment
│
├── requirements.txt
├── manage.py
├── .gitignore
├── .env
└── README.md
