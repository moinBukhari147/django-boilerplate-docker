# 🚀 Django Dockerized Boilerplate

A **production-ready Django boilerplate** designed for rapid backend development, following clean architecture, strict linting, and scalable async processing.

---

## ✨ Features

### 🧹 Code Quality & Developer Experience
- **Ruff** configured via `ruff.toml` for linting & clean code
- **Pre-commit hooks** to enforce linting before pushes
- **VS Code settings & extensions** included in .vscode folder
- **uv** for fast dependency management (local & Docker)
- Structured apps-based architecture
- Separate settings for `base`, `dev`, `stage`, and `prod`

---

### 🛡 Security & Best Practices
- Custom **DRF exception handler** with a consistent API error format
- Standardized **success response renderer**
- Environment-based configuration using **django-environ**
- Database configuration via **dj-database-url**
- Secure Dockerized runtime
- Custom exception classes beyond DRF defaults

---

### 🗄 Database
- PostgreSQL support
- URL-based DB configuration using `dj-database-url`
- Environment-aware DB switching

---

### 🧵 Async Tasks & Background Jobs
- **Celery** configured for background processing
- **Redis** as message broker
- **Flower** dashboard with basic authentication
- Retry & failure tracking for jobs

---

### 🧪 Testing & CI/CD
- **pytest** fully configured for Django
- Global `conftest.py` shared across all apps
- Separate test file per endpoint
- Tests only run inside **development Docker image**
- CI pipeline runs tests on PR creation and merge
- Merge blocked unless tests pass
- CI currently on `main` (can be moved to `dev`)
- `stage` & `main` branches has to be intended for image build & push

---

## 📂 Project Structure
django-boilerplate-docker/
```
│── apps/
│ ├── core/
│ │ ├── migrations/
│ │ ├── models/
│ │ │  ├── base.py/
│ │ │  ├── example.txt/
│ │ │  └── soft_delete.py/
│ │ ├── tests/
│ │ ├── admin.py
│ │ ├── app.py
│ │ ├── exception.py
│ │ ├── renderer.py
│ │ └── urls
│ │ └── views.py
│ ├── app_one/
│ │ ├── models/
│ │ │ ├── model_1.py
│ │ │ └── model_2.py
│ │ ├── v1/
│ │ │ ├── serializers/
│ │ │ │ ├── serializers_1.py
│ │ │ │ └── serializers_2.py
│ │ │ ├── views/
│ │ │ │ ├── views_1.py
│ │ │ │ └── views_2.py
│ │ │ └── urls.py
│ │ └── tests/
│ │ │ │ ├── test_api_1.py
│ │ │ │ └── test_api_2.py
│ ├── conftest.py
│── config/
│ ├── env/
│ │ └── sample_env.txt
│ ├── settings/
│ │ ├── base.py
│ │ ├── dev.py
│ │ ├── stage.py
│ │ └── prod.py
│ │── asgi.py
│ │── celery.py
│ │── urls.py
│ │── wsgi.py
│── static/
│── media/
│── .dockerignore
│── .gitignore
│── .pre-commit-config.yaml
│── .python-version
│── Dockerfile
│── Makefile
│── README.md
│── docker-compose.yml
│── manage.py
│── pyproject.toml
│── ruff.toml
│── .github/
│ └── workflows/
│── .vscode/
│ │── settings.json
│ └── extension.json
```


---

## 🧱 Application Architecture Guidelines

### 📌 Models
- Each app has a **models folder**, not a single file
- One model per file
- Related models grouped inside the same app

```
apps/core/models/
├── base.py
├── user.py
└── audit_log.py
```


---

### 📌 APIs & Versioning
- Each API version has its own folder (`v1`, `v2`, etc.)
- Inside each version:
  - `serializers/`
  - `views/`
  - `urls.py`

```
apps/property/v1/
├── serializers/
├── views/
└── urls.py
```


**Guidelines**
- Max **4–5 views/serializers per file**
- Group logically related endpoints together
- Avoid dumping all endpoints into one file

---

### 📌 Tests
- Each endpoint has its **own test file**
- Tests live inside the app

```
apps/property/tests/
├── test_create_property.py
├── test_update_property.py
└── test_delete_property.py
```


- Global fixtures available via shared `conftest.py`

---

## 📦 API Response Standard

### ✅ Success Response
```json
{
  "success": true,
  "status_code": 200,
  "message": "Request processed successfully.",
  "data": {}
}
```
## ❌ Error Response
```
{
  "success": false,
  "status_code": 400,
  "code": "validation_error",
  "error": {
    "field": ["This field is required."]
  }
}
```

# 🚀 Getting Started

This project uses **uv** for dependency management and **Docker + Docker Compose** for running services.
You do **not** need to create or activate a virtual environment — **uv manages it automatically**.

---

## 🧰 Prerequisites

* Python **3.11+**
* **uv**
* **Docker** & **Docker Compose**

### Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv --version
```

---

### 🐍 Python Version Setup (uv)

Set a specific Python version for the project using **uv**:

```bash
# List available versions
uv python list

# Install a specific version
uv python install 3.11.9

# Use it for the project
uv python pin 3.11.9

# Install the latest Python version available
uv python install

# Use it for the project
uv use latest

# Verify
uv run python --version

```

---

## 🔄 Dependency Setup (Required)

Always sync dependencies before starting the project (local or Docker):

```bash
uv sync
```

If `pyproject.toml` changes:

```bash
uv lock
uv sync
```

Upgrade all dependencies to the latest stable versions:

```bash
uv lock --upgrade
uv sync
```
- Updates uv.lock with the latest stable versions
- Respects version constraints in pyproject.toml
- Requires review + testing before commit


Upgrade a specific dependency:

```bash
uv lock --upgrade django
uv sync
```
- Updates uv.lock with the latest stable versions
- Respects version constraints in pyproject.toml
- Requires review + testing before commit

---

## 🔐 Environment Variables

```bash
cp config/env/.sample_env .env
```

You can update the env according to your needs.

---

## 🧠 Local Usage (uv only)

Use this for **IntelliSense, pre-commit, and linting.

In order to run any command using uv below are the examples.

```bash
uv run python manage.py migrate
uv run python manage.py createsuperuser
uv run python manage.py runserver
```

---

## 🐳 Docker Usage (Recommended)

### Build & Start

```bash
make build
make up
```

### 🐳 Docker Python Version

The Dockerfile uses a specific Python base image.  
If you change the Python version for local development with `uv`, update the `FROM` line in the Dockerfile to match:

```dockerfile
FROM python:3.11.9-slim  # update to match uv Python version
```

### Migrations & Admin

```bash
make migrate
make createsuperuser
```

---

## 🌸 Celery & Flower

```bash
make celery-worker
make celery-beat
make flower
```

Flower UI:

```
http://localhost:5555
```

---

## 🧪 Tests

```bash
make test
```

Runs migrations, tests with coverage, generates `htmlcov/`, then shuts down containers.

---

## 🧹 Important Make Commands

```bash
make up          # start all services
make down        # stop services
make downv       # stop + remove volumes
make restart     # restart containers
make logs        # all logs
make djangologs  # django logs only
make dcshell     # django container shell
make prune       # docker cleanup
make psql        # postgres shell
make rediscli    # redis cli
```


