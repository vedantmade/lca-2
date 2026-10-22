# Financial Clarity Web App

A modern, high-performance web version of the **Financial Clarity** expense tracker and tag manager application. Built with a **Python FastAPI** backend and a modern **Tailwind CSS + JavaScript (SPA)** frontend matching the Stitch Neo-Brutalist design system.

---

## 🌟 Features

- 📊 **Financial Dashboard**:
  - Month and time range selectors
  - Bento Grid summary cards (Total Spent, Top Expense)
  - Interactive SVG Donut Spending Breakdown Chart
  - Interactive Daily Trend Bar Chart (7-day history)
  - Untagged transactions review banner
  - Operations / Recent transactions list
- 📜 **History & Transactions**:
  - Instant search filtering by merchant name or notes
  - Filter pills for categories (All, Untagged, Food, Transport, Subscriptions, etc.)
  - Transactions grouped by date (TODAY, YESTERDAY, EARLIER)
  - Quick tag assignment and transaction deletion
- 🏷️ **Tag Manager**:
  - Custom category tags with names, emojis, and hex color codes
  - Transaction count and spending calculation per tag
  - Create, edit, and delete tags
- ⚡ **Auto-Tag Rules**:
  - Keyword-based auto-tagging rules (e.g., keyword `ZOMATO` -> tag `Food`)
  - One-click rule execution across existing untagged transactions
- 🌓 **Light & Dark Theme**: Toggle between light mode and dark mode with persistent settings.

---

## 📁 Directory Structure

```
web_app/
├── backend/
│   ├── main.py          # FastAPI application entry point & routes
│   ├── database.py      # SQLite database engine configuration
│   ├── models.py        # SQLAlchemy ORM models (Transaction, Tag, AutoTagRule)
│   ├── schemas.py       # Pydantic validation schemas
│   ├── crud.py          # Database operations & dashboard analytics calculation
│   ├── seed_data.py     # Default tags, rules, and demo transactions seeder
│   ├── requirements.txt # Python dependencies
│   └── expense_tracker.db # SQLite Database file (created on launch)
├── frontend/
│   ├── index.html       # Single Page Application HTML structure
│   ├── css/
│   │   └── styles.css   # Modern Tailwind CSS & chart styling
│   └── js/
│       ├── api.js       # Frontend API client
│       └── app.js       # SPA tab router, state management & DOM renderer
└── run.py               # Application runner script
```

---

## 🚀 How to Run

### 1. Install Dependencies
```bash
cd web_app/backend
pip install -r requirements.txt
```

### 2. Start Application
From the `web_app` directory, run:
```bash
python run.py
```
Or directly from `web_app/backend`:
```bash
python main.py
```

The FastAPI backend will launch on `http://127.0.0.1:8000` and automatically serve the web application frontend at `http://127.0.0.1:8000`.

---

## CI/CD Pipeline (CCA-2)

**Flow:** GitHub → Jenkins (EC2) → Build/Test → Docker image → Amazon ECR → Minikube (Deployment + Service) → Verify

| Stage | What it does |
|---|---|
| Checkout | Jenkins pulls the latest code from GitHub |
| Build & Test | venv, install deps, `compileall` syntax check, `pytest tests/` smoke tests |
| Docker Build | Builds the image from `Dockerfile`, tagged `v<BUILD_NUMBER>` and `latest` |
| Push to ECR | Logs in with the EC2 IAM role (no stored keys) and pushes both tags |
| Deploy to Minikube | Refreshes `ecr-secret`, applies `k8s/deployment.yaml` (image substituted) and `k8s/service.yaml` |
| Verify | `kubectl get pods/deployment/svc`, rollout status, curl via port-forward |

- Image tag = build number, for traceability and easy rollback.
- App listens on port 8000; Service is NodePort 30080 (port 80 → 8000).
- Access: `kubectl port-forward --address 0.0.0.0 svc/upiwhere-svc 8081:80`, then open `http://<EC2_PUBLIC_IP>:8081`.
- Run locally: `docker build -t upiwhere . && docker run -p 8000:8000 upiwhere`.
