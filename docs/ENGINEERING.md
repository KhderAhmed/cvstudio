# Engineering notes

## Quick start

Requirements: Python 3.12, Node.js 22.18+, and the system libraries required by WeasyPrint (see `backend/Dockerfile`).

From the repository root:

```bash
# API
cd backend
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

# Frontend
cd ../frontend
npm ci
npm run dev