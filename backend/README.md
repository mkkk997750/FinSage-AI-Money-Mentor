# FinSage Backend

This is the backend for **FinSage – AI Money Mentor**, built with FastAPI and PostgreSQL.

## Features

- REST API for financial analysis, planning, and agent orchestration
- Multi-agent architecture using LangGraph and LangChain
- Google Gemini and OpenAI LLM support
- PostgreSQL database with rich schema (see `../data/schema.sql`)
- Modular routers for agents, data, and user management

## Requirements

- Python 3.10+
- PostgreSQL 13+

## Setup

1. **Clone the repo and enter backend:**
   ```sh
   cd backend
   ```
2. **Create a virtual environment and activate it:**
   ```sh
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # or
   source .venv/bin/activate  # Linux/Mac
   ```
3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
4. **Configure environment variables:**
   - Copy `.env.example` to `.env` and fill in your values (API keys, DB credentials).

5. **Set up the PostgreSQL database:**
   - Create the database (default: `finsage`).
   - Run the schema:
     ```sh
     psql -U postgres -d finsage -f ../data/schema.sql
     psql -U postgres -d finsage -f ../data/seed_data.sql  # (optional demo data)
     ```

6. **Run the backend server:**
   ```sh
   uvicorn main:app --reload
   # Or from project root:
   uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
   ```

## API Docs

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- Redoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Project Structure

- `main.py` – FastAPI entrypoint
- `models.py` – Pydantic models
- `routers/` – API routers (agents, data)
- `src/` – DB, nodes, tools, state, config
- `requirements.txt` – Python dependencies

## License

MIT
