# Promptory

Promptory is a Django web application for writing, improving, and organizing AI prompts. It evaluates prompt quality, suggests missing details, and generates an optimized version using common prompt-engineering techniques.

## Features

- User registration, login, and logout
- Prompt scoring based on task, context, output format, and detail
- Prompt suggestions for improving clarity and specificity
- Optimization techniques:
  - Zero-shot prompting
  - Role prompting
  - Few-shot prompting
  - Structured output prompting
- Prompt history saved per user
- Categories for coding, study, interviews, content, data, and general prompts
- Favorite prompts, search, and category/favorite filtering
- Reusable prompt templates managed through the Django admin
- Optional OpenAI API smoke test

## Tech Stack

- Python
- Django 6.1
- SQLite for local development
- HTML and CSS templates
- `python-dotenv` for environment variables
- OpenAI Python SDK for the optional API test

## Requirements

- Python 3.12 or newer
- A virtual environment is recommended
- An OpenAI API key is only required for `test_openai.py`; the main prompt scoring and optimization workflow is local

## Setup

### 1. Create and activate a virtual environment

PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Command Prompt:

```bat
python -m venv venv
venv\Scripts\activate
```

### 2. Install dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 3. Configure environment variables

Create a local `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

Never commit `.env` or paste an API key directly into source code. The file is ignored by Git.

### 4. Apply database migrations

```powershell
python manage.py migrate
```

### 5. Create an administrator account (optional)

```powershell
python manage.py createsuperuser
```

### 6. Start the development server

```powershell
python manage.py runserver
```

Open <http://127.0.0.1:8000/> in a browser.

## Main URLs

| URL | Purpose |
| --- | --- |
| `/` | Public Promptory home page |
| `/accounts/signup/` | Create an account |
| `/accounts/login/` | Log in |
| `/accounts/logout/` | Log out |
| `/accounts/dashboard/` | Create, score, optimize, and manage prompts |
| `/admin/` | Django administration |

## Testing

Run the Django test suite with:

```powershell
python manage.py test
```

The current tests cover prompt scoring, score comparison, and a valid dashboard submission.

## Optional OpenAI API Test

`test_openai.py` makes a small request through the OpenAI Responses API:

```powershell
python test_openai.py
```

The script uses the model configured in that file. Change the model name if it is unavailable for your account or has been retired. This script is separate from the local Django prompt optimization workflow.

## Project Structure

```text
.
├── accounts/                 Authentication, views, models, forms, and tests
├── promt_engineering/        Django project settings and URL configuration
├── templates/accounts/       HTML templates for the application
├── manage.py                 Django command-line entry point
├── test_openai.py            Optional OpenAI API smoke test
├── db.sqlite3                Local development database (ignored by Git)
└── .env                      Local environment variables (ignored by Git)
```

## Production Notes

This project is configured for local development. Before deploying, move `SECRET_KEY` and other sensitive settings to environment variables, set `DEBUG = False`, configure `ALLOWED_HOSTS`, use a production database, and follow Django's deployment checklist.
