# 🎨 CV Studio: Your Living Resume

> An Arabic-first platform for building smart resumes, with voice intros, video, ATS analysis, and PDF export.

![Django](https://img.shields.io/badge/Django-5.0-green)
![Vue](https://img.shields.io/badge/Vue-3.5-brightgreen)
![DRF](https://img.shields.io/badge/DRF-3.15-red)
![License](https://img.shields.io/badge/License-MIT-blue)

---

## 📖 Overview

**CV Studio** is a full-stack web platform for building **living** resumes. Instead of a static PDF, you get an interactive web page that updates in real time and can be shared with a single link.

### ✨ Key Features

| Feature | Description |
|---|---|
| 📄 **Living Resume** | An interactive web page with a permanent shareable link |
| 🎙️ **Text to Speech** | Turn your summary into a spoken introduction using gTTS |
| 🎥 **Intro Video** | Upload a video or embed a YouTube link |
| 🎯 **ATS Analysis** | Score how well your resume matches a job description (English and Arabic keywords) |
| 📑 **PDF Export** | Text-based PDF that works with applicant tracking systems |
| 📊 **Analytics** | Track resume views (device, time, source) |
| 👥 **Roles** | Admin (full management) / User (own resume only) |
| 🌐 **Arabic First** | Full RTL interface with Arabic TTS support |

---

## 🛠️ Tech Stack

### Backend
- **Python 3.12**, **Django 5.0**, **DRF 3.15**
- **JWT** authentication (SimpleJWT)
- **gTTS** for text-to-speech
- **WeasyPrint** for PDF export
- **PostgreSQL** (SQLite also supported)
- **CORS** and **WhiteNoise**

### Frontend
- **Vue 3.5** with the **Composition API**
- **Vite** as the build tool
- **Vue Router** and **Pinia**
- **TailwindCSS 4** (RTL-ready design)
- **Chart.js** for charts
- **Axios** for API requests

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 22.18+ (or 24.12+)
- **PDF export (Windows only):** WeasyPrint needs the GTK/Pango runtime installed. See the [WeasyPrint installation guide](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html). On Linux or Docker the Dockerfile already installs everything, including Arabic fonts.

### 1. Backend (Django)

```bash
cd backend
python -m venv venv

# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### 2. Frontend (Vue)

```bash
cd frontend
npm install
npm run dev
```

### 3. Environment variables (optional locally, required in production)

| Variable | Default | Description |
|---|---|---|
| `DEBUG` | `True` | Set to `False` in production |
| `SECRET_KEY` | dev-only key | **Required** when `DEBUG=False` |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` | Comma-separated hosts |
| `CORS_ALLOWED_ORIGINS` | `http://localhost:5173,http://127.0.0.1:5173` | Comma-separated origins |
| `CSRF_TRUSTED_ORIGINS` | _(empty)_ | Comma-separated origins (needed for `/django-admin/` login behind a proxy) |
| `USE_HTTPS` | `False` | `True` enables secure cookies and the proxy SSL header |
| `POSTGRES_HOST` | _(unset → SQLite)_ | Set to use PostgreSQL |
| `POSTGRES_DB` / `POSTGRES_USER` / `POSTGRES_PASSWORD` / `POSTGRES_PORT` | `cvstudio` / `cvstudio` / _(empty)_ / `5432` | PostgreSQL connection |

### 4. Open in the browser

- Frontend: http://localhost:5173
- API: http://localhost:8000/api/
- Django Admin: http://localhost:8000/django-admin/

---

## 🐳 Docker (production-like)

Runs PostgreSQL, the Django API (gunicorn + WhiteNoise) and the Vue app behind nginx. Everything is served from one origin on port 80.

```bash
cp .env.example .env     # then edit the values (SECRET_KEY, POSTGRES_PASSWORD, ALLOWED_HOSTS...)
docker compose up -d --build
docker compose exec backend python manage.py createsuperuser
```

- App: http://localhost
- Django Admin: http://localhost/django-admin/
- Uploaded files are kept in the `media_files` volume, the database in `postgres_data`.
- Behind HTTPS, set `USE_HTTPS=True` and use `https://` origins in `CORS_ALLOWED_ORIGINS` and `CSRF_TRUSTED_ORIGINS`.

---

## 📁 Project Structure

```text
cvstudio/
├── backend/                  # Django
│   ├── accounts/             # Users and authentication
│   ├── resumes/              # Resumes, experience, skills
│   ├── analytics/            # View statistics
│   ├── cvstudio_backend/     # Project settings
│   ├── Dockerfile
│   ├── entrypoint.sh
│   └── requirements.txt
├── frontend/                 # Vue
│   ├── src/
│   │   ├── views/            # Pages
│   │   ├── components/       # Components
│   │   ├── stores/           # Pinia stores
│   │   ├── router/           # Vue Router
│   │   └── api/              # Axios client
│   ├── Dockerfile
│   ├── nginx.conf
│   └── package.json
└── README.md
```

---

## 🔌 Main API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/register/` | Register a new user |
| POST | `/api/token/` | Log in (JWT) |
| POST | `/api/token/refresh/` | Refresh the access token |
| GET | `/api/users/me/` | Current user data |
| GET/POST | `/api/resumes/` | List / create resumes |
| GET/PUT/PATCH/DELETE | `/api/resumes/<id>/` | Retrieve / update / delete a resume |
| CRUD | `/api/experiences/`, `/api/skills/`, `/api/certificates/`, `/api/links/` | Resume sections (own resumes only) |
| POST | `/api/resumes/<id>/tts/` | Generate audio |
| POST | `/api/resumes/<id>/ats/` | Run ATS analysis |
| GET | `/api/resumes/<id>/pdf/` | Export PDF (owner) |
| GET | `/api/public/resumes/<id>/` | Public resume |
| GET | `/api/public/resumes/<id>/pdf/` | Public resume PDF |
| GET | `/api/analytics/resumes/<id>/` | Analytics for one resume |
| GET | `/api/analytics/me/` | Analytics across all your resumes |
| GET | `/api/admin/stats/` | Platform statistics (Admin) |
| GET | `/api/admin/users/` | All users (Admin) |
| PATCH | `/api/admin/users/<id>/toggle/` | Activate / deactivate a user (Admin) |
| GET | `/api/admin/resumes/` | All resumes (Admin) |
| DELETE | `/api/admin/resumes/<id>/delete/` | Delete a resume (Admin) |

---|---|---|
| POST | `/api/auth/register/` | Register a new user |
| POST | `/api/token/` | Log in (JWT) |
| GET | `/api/users/me/` | Current user data |
| GET/POST | `/api/resumes/` | List / create resumes |
| GET/PUT | `/api/resumes/<id>/` | Retrieve / update a resume |
| POST | `/api/resumes/<id>/tts/` | Generate audio |
| POST | `/api/resumes/<id>/ats/` | Run ATS analysis |
| GET | `/api/resumes/<id>/pdf/` | Export PDF |
| GET | `/api/public/resumes/<id>/` | Public resume |
| GET | `/api/analytics/resumes/<id>/` | Resume analytics |
| GET | `/api/admin/stats/` | Platform statistics (Admin) |

---

## 🎯 ATS Algorithm

The ATS analyzer measures how well a resume matches a job description:

1. Extract keywords from the job description (excluding stop words)
2. Compare them against the resume text (summary, experience, skills, certifications)
3. Calculate a match percentage, with bonuses and penalties based on content quality
4. Suggest missing keywords

**Result:** a score from 0 to 95, plus lists of matched and missing keywords.

---

## 🖼️ Screenshots

Coming soon.

---

## 🤝 Contributing

Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 👤 Author

**Khder Ahmed**

- GitHub: [@KhderAhmed](https://github.com/KhderAhmed)
- LinkedIn: [khder-ahmed](https://linkedin.com/in/khder-ahmed-b46274286)

---

## 🌟 Support

If you like this project, give it a ⭐ on GitHub. It helps me keep improving it.
