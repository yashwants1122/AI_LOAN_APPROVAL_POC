# 🏦 SmartLoan AI — Two-Agent Loan Approval System

A simple customer-facing Streamlit application demonstrating a two-agent loan approval workflow.

## Agents

### Agent 1 — Credit Risk Agent
Checks:
- Credit/CIBIL score
- Payment defaults
- Existing EMI vs income
- Basic credit risk

### Agent 2 — Loan Decision Agent
Checks:
- Credit risk from Agent 1
- Employment experience
- Basic affordability
- Requested loan amount

Possible results:
- ✅ APPROVED
- 🟠 REVIEW
- ❌ REJECTED

## Run in VS Code / PowerShell

Open the project folder in VS Code.

### 1. Create virtual environment

```powershell
python -m venv .venv
```

### 2. Activate it

```powershell
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Start Streamlit

```powershell
streamlit run app.py
```

The application will open in your browser.

## Deploy to Streamlit Community Cloud

1. Create a GitHub repository.
2. Upload:
   - `app.py`
   - `requirements.txt`
   - `README.md`
3. Go to Streamlit Community Cloud.
4. Create a new app.
5. Select your GitHub repository.
6. Set the main file to:

```text
app.py
```

7. Deploy.

No API key or secret is required for this demo because the two agents use transparent Python decision logic.

## Important

This is a demonstration/pre-approval application. It is not a production banking credit decision engine.
