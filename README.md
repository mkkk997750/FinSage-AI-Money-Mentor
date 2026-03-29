# FinSage – AI Money Mentor

**FinSage** is a multi-agent AI-powered financial advisor platform for personalized money management, built for the ET AI Hackathon 2026.

## Overview

- **Backend:** FastAPI, LangGraph, LangChain, PostgreSQL
- **Frontend:** React, Vite, Chart.js
- **Agents:** Health Score, FIRE Planner, Tax Wizard, Insurance Audit, Life Event, Couple Planner, MF X-Ray, Full Analysis

### Detailed Agent Breakdown

1. **Health Score Agent:** Evaluates the user's overall financial health based on income, expenses, assets, and liabilities, generating a comprehensive financial health score out of 100.

2. **FIRE Planner (Financial Independence, Retire Early):** Calculates required SIPs and investment strategies to achieve early retirement goals, projecting corpus requirements.

4. **Tax Wizard:** Analyzes the user's income and current investments (like 80C, NPS, etc.) to suggest actionable tax-saving strategies and optimize tax liabilities.

5. **Insurance Audit:** Reviews existing insurance policies (Life, Health, Term) and recommends appropriate coverage amounts based on dependencies and lifestyle.

6. **Life Event Planner:** Helps users financially plan for major life milestones like marriage, having a baby, purchasing a house, or managing a sudden bonus.

7. **Couple Planner:** Designed for couples to manage joint finances, define shared goals, and consolidate their savings and investment strategies.

8. **MF X-Ray (Mutual Fund Portfolio Analyzer):** Evaluates the user's mutual fund investments, checking portfolio overlap, risk ratios, and suggesting optimal asset allocation.

9. **Full Analysis:** An orchestrator agent that aggregates findings from all other agents to deliver a complete, end-to-end holistic financial report.
## Quick Start

### 1. Backend

- Python 3.10+, PostgreSQL 13+
- See `backend/README.md` for full setup

### 2. Frontend

- Node.js 18+, npm 9+
- See `frontend/README.md` for full setup

### 3. Database

- PostgreSQL schema in `data/schema.sql`
- (Optional) Demo data in `data/seed_data.sql`

## Running Locally

1. **Start PostgreSQL and create the database:**
   ```sh
   createdb finsage
   psql -U postgres -d finsage -f data/schema.sql
   psql -U postgres -d finsage -f data/seed_data.sql  # (optional)
   ```
2. **Backend:**
   ```sh
   cd backend
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   uvicorn main:app --reload
   # Or from project root:
   uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
   ```
3. **Frontend:**
   ```sh
   cd frontend
   npm install
   npm run dev
   # App at http://localhost:3000
   ```

## Folder Structure

- `backend/` – FastAPI app, agents, DB, routers
- `frontend/` – React app, UI, API client
- `data/` – PostgreSQL schema and seed data

## License

MIT
