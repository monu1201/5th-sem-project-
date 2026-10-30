# AI-Powered Intelligent Code Review and Software Defect Prediction System

[![Python Version](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.3-61DAFB.svg)](https://react.dev/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-1.4+-F7931E.svg)](https://scikit-learn.org/)
[![Database](https://img.shields.io/badge/Database-MySQL%20%7C%20SQLite%20Fallback-4479A1.svg)](https://www.mysql.com/)

A full-stack, enterprise-grade developer tool for automated code inspection, software defect risk prediction, static AST security auditing, and intelligent fix generation.

---

## 1. System Architecture & Workflow

The platform implements a continuous six-stage pipeline:

```
Source Code Input
      │
      ▼
Preprocessing & Language Detection  (Size check, safe sanitization, token analysis)
      │
      ▼
AST Static Analysis  (Bare except, mutable defaults, SQL injections, eval, buffer overflows)
      │
      ▼
AI Code Review  (Multi-provider abstraction: Gemini, OpenAI, Claude, Ollama, Offline Engine)
      │
      ▼
Feature Extraction & ML Defect Prediction  (McCabe Cyclomatic, Halstead, Nesting, LOC → Random Forest)
      │
      ▼
Result Aggregation & Quality Scoring  (Normalized 0-100 Score, Low/Medium/High Risk categorization)
      │
      ▼
Developer Feedback & Actionable Remediation  (Side-by-side diff, recommendations, PDF/MD/JSON audit export)
```

---

## 2. Core Features

1. **Multi-Language Support**: Full AST and pattern analyzers for **Python**, **JavaScript/TypeScript**, **Java**, and **C++**.
2. **Defect Detection & Security Auditing**:
   - **Bugs**: Bare exception handling, mutable default parameters, unhandled promises, null pointer risks.
   - **Security Flaws**: Raw SQL string concatenation, unsafe `eval()`/`exec()`, hardcoded credentials, buffer overruns (`strcpy`), and XSS injection patterns.
   - **Code Smells**: Deeply nested control flows, long methods, high cyclomatic complexity, loose equality coercions.
3. **Machine Learning Defect Scoring**:
   - Random Forest and Logistic Regression classifiers trained on software metric distributions (NASA MDP/PROMISE metrics: McCabe cyclomatic complexity, Halstead volume, nesting depth, LOC).
   - Generates Defect Probability (0–100%) and Defect-Prone binary classification.
   - Risk categorization: **0–30% Low**, **31–60% Medium**, **61–100% High**.
4. **Multi-Model AI Abstraction Layer**:
   - Pluggable providers: Google Gemini, OpenAI, Anthropic Claude, Ollama, and an offline **Deterministic Rule-Based Review Engine** (guarantees full functionality with zero API keys).
5. **Code Comparison & Suggested Fix**:
   - Side-by-side split visual diff highlighting original flawed code alongside refactored, hardened replacement code.
6. **Executive Dashboard & Visualizations**:
   - KPI metrics (total reviews, critical issues, high-risk files, avg quality score, avg defect probability).
   - Interactive charts for severity distribution, quality trends, and risk proportions.
7. **Audit Report Export**:
   - Export formal reports as **Markdown (.md)**, **Printable HTML / PDF**, or **Structured JSON**.
8. **Pre-Loaded Sample Vulnerabilities**:
   - One-click "Try Sample Code" loader for quick testing across all supported languages.

---

## 3. Project Structure

```
ai-code-review-system/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── endpoints.py           # REST API endpoints (/api/analyze, /api/dashboard, etc.)
│   │   ├── core/
│   │   │   └── config.py              # Application settings and environment parsing
│   │   ├── database/
│   │   │   └── session.py             # SQLAlchemy session and intelligent MySQL/SQLite fallback
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── entities.py            # ORM entities (Reviews, Issues, Predictions, Recommendations)
│   │   ├── schemas/
│   │   │   └── schemas.py             # Pydantic v2 validation models
│   │   ├── services/
│   │   │   ├── preprocessor.py        # Untrusted input sanitization & metric parser
│   │   │   ├── static_analyzer.py     # AST-based multi-language vulnerability visitor
│   │   │   ├── aggregator.py          # Merges AI, ML, and AST signals into quality score
│   │   │   └── report_generator.py    # Generates Markdown and HTML audit reports
│   │   └── main.py                    # FastAPI application initialization & CORS
│   ├── tests/
│   │   └── test_pipeline.py           # Unit and integration pytest test suite
│   └── requirements.txt               # Backend Python dependencies
├── ml/
│   ├── data/
│   │   └── generate_dataset.py        # NASA/PROMISE benchmark distribution generator
│   ├── models/
│   │   ├── defect_model.joblib        # Serialized Random Forest model
│   │   ├── metrics_scaler.joblib      # StandardScaler artifact
│   │   └── model_metadata.json        # Training metrics (Accuracy, ROC-AUC, F1-score)
│   ├── feature_extraction.py          # Cyclomatic complexity, Halstead, nesting depth
│   ├── preprocessing.py               # Feature normalization & vector scaling
│   ├── model.py                       # Model factory & risk classification logic
│   ├── train.py                       # Model training & hyperparameter optimization
│   ├── predict.py                     # Real-time inference & risk factor identifier
│   └── evaluate.py                    # Classification report & confusion matrix evaluation
├── ai_engine/
│   ├── base.py                        # BaseAIReviewer interface
│   ├── prompts.py                     # Structured JSON prompts
│   ├── provider.py                    # Gemini, OpenAI, Claude, Ollama, & Rule-Based providers
│   └── reviewer.py                    # Review orchestrator with fallback resilience
├── database/
│   └── schema.sql                     # Full MySQL 8 DDL database schema
├── samples/
│   ├── sample_python_vulnerable.py    # SQL injection, eval, bare except, mutable default
│   ├── sample_javascript_smelly.js    # Loose equality, eval, DOM XSS
│   ├── sample_java_leak.java          # Hardcoded password, unclosed stream
│   └── sample_cpp_buffer.cpp          # Buffer overflow (strcpy), memory leak
├── frontend/
│   ├── src/
│   │   ├── components/                # Navbar, Sidebar, CodeEditor, DiffViewer, ScoreCard, Charts
│   │   ├── pages/                     # LandingPage, Dashboard, CodeReview, ResultDetail, History
│   │   ├── services/api.js            # Axios REST API client
│   │   ├── App.jsx                    # Router & Dashboard layout
│   │   ├── index.css                  # Tailwind styles & dark developer theme tokens
│   │   └── main.jsx                   # React root entrypoint
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── Dockerfile
├── .env.example                       # Environment configuration template
├── docker-compose.yml                 # Multi-container orchestration (MySQL + Backend + Frontend)
├── Dockerfile                         # Backend container Dockerfile
└── README.md
```

---

## 4. Prerequisites

- **Python 3.11+** (Python 3.11, 3.12, or 3.13)
- **Node.js 18+** and **npm**
- *(Optional)* **MySQL 8.0+** or **Docker Desktop** (if you wish to use MySQL instead of the automatic SQLite zero-config fallback)

---

## 5. Local Setup in VS Code (Windows / PowerShell)

### Step 1: Clone or Open Project
Open the project directory in VS Code:
```powershell
code .
```

### Step 2: Configure Environment Variables
Copy `.env.example` to `.env`:
```powershell
Copy-Item .env.example .env
```
Open `.env` and configure your preferences:
- To use an AI provider, set `AI_PROVIDER=gemini` (or `openai`) and supply `AI_API_KEY`.
- If you don't have an AI API key, leave `AI_API_KEY=` blank; the system will automatically utilize the built-in local AST rule engine with zero friction.

### Step 3: Install Backend Dependencies & Train ML Model
In your PowerShell terminal:
```powershell
python -m pip install -r backend/requirements.txt
```
Train the ML defect prediction model:
```powershell
python -m ml.train
```

### Step 4: Run Backend Server
Start the FastAPI server on port 8000:
```powershell
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```
You can verify the backend is online by visiting [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) in your browser.

### Step 5: Install Frontend Dependencies & Start Dev Server
Open a second terminal in VS Code:
```powershell
cd frontend
npm install
npm run dev
```
Open [http://localhost:5173](http://localhost:5173) in your browser.

---

## 6. Database Setup

The backend features an **intelligent dual-engine database layer**:
1. **Primary Target (MySQL 8.0)**:
   - If MySQL is installed locally (e.g. via XAMPP, MySQL Server, or Docker), create the database:
     ```sql
     CREATE DATABASE code_review_db;
     ```
   - Set `DATABASE_URL=mysql+pymysql://root:password@localhost:3306/code_review_db` in `.env`.
   - The tables will be auto-migrated on startup, or you can run `database/schema.sql`.
2. **Automatic Zero-Config Fallback (SQLite)**:
   - If MySQL is offline or not installed, the backend detects connection failure and gracefully falls back to `sqlite:///./app.db`.
   - All tables and relationships are created automatically without manual configuration.

---

## 7. Running with Docker Compose

To launch the complete stack (MySQL 8, FastAPI Backend, and React Frontend in Nginx) with a single command:

```bash
docker-compose up --build
```

- **Frontend**: [http://localhost:5173](http://localhost:5173)
- **Backend API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **MySQL Database**: `localhost:3306` (`code_review_db`)

---

## 8. REST API Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/health` | System readiness, active database type, and ML model status |
| `POST` | `/api/analyze` | Complete pipeline: static analysis, AI review, ML defect scoring, persistence |
| `POST` | `/api/review` | AI code review execution only |
| `POST` | `/api/predict` | ML software defect probability prediction only |
| `GET` | `/api/reviews` | List past code reviews with filtering (risk level, language, search) |
| `GET` | `/api/reviews/{id}` | Detailed review report with issues, metrics, and suggested code |
| `DELETE` | `/api/reviews/{id}` | Delete a code review record |
| `GET` | `/api/reviews/{id}/report` | Download report in `markdown`, `html`, or `json` format |
| `GET` | `/api/dashboard` | Aggregated KPI statistics, risk distribution, and severity breakdown |
| `GET` | `/api/samples` | Fetch pre-configured sample files with intentional vulnerabilities |

---

## 9. Running Automated Tests

Run the test suite using pytest:
```powershell
python -m pytest backend/tests -v
```

This verifies:
- Language detection heuristics
- Preprocessor input size boundaries
- Python AST security & bug visitors (eval, bare except, mutable default)
- JavaScript static rules (eval, loose equality)
- ML model prediction and probability bounds
- API health and end-to-end code submission flow

---

## 10. Security & Untrusted Code Execution

- **Zero Host Execution**: User-submitted code is **strictly parsed as data** via lexical tokens, AST syntax nodes, and language visitors. Submitted code is **NEVER** executed on the host system.
- **Request Boundaries**: Max file size is capped at 500 KB to defend against memory exhaustion attacks.
- **Credential Protection**: API keys and secrets are loaded from environment variables or per-request headers and never committed to source control.
- **Sanitized Outputs**: Filenames and user parameters are validated and escaped.

---

## 11. Future Improvements

- Integration with GitHub / GitLab Pull Request webhooks for automated CI/CD gating.
- Git repository cloning and multi-file project workspace analysis.
- Graph-based dependency vulnerability auditing (CVE lookup against lockfiles).
