"""
FastAPI Main Application — FinSage AI Money Mentor
ET AI Hackathon 2026
"""
from __future__ import annotations

import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from routers.agents import router as agents_router
from routers.data import router as data_router

# ─── App Setup ────────────────────────────────────────────────────────────────

app = FastAPI(
    title="FinSage — AI Money Mentor",
    description="ET AI Hackathon 2026 | Multi-Agent LangGraph Financial Advisor",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Include Routers ──────────────────────────────────────────────────────────
app.include_router(agents_router)
app.include_router(data_router)

# ─── Serve Frontend (production build) ────────────────────────────────────────
FRONTEND_DIST = Path(__file__).parent.parent / "frontend" / "dist"

if FRONTEND_DIST.exists():
    app.mount("/assets", StaticFiles(directory=str(FRONTEND_DIST / "assets")), name="assets")

    @app.get("/", include_in_schema=False)
    def serve_frontend():
        return FileResponse(str(FRONTEND_DIST / "index.html"))

# ─── Health Check ─────────────────────────────────────────────────────────────

@app.get("/api/health")
def health_check():
    """Health check endpoint — verifies DB connection."""
    try:
        from src.db import fetch_one
        result = fetch_one("SELECT COUNT(*) as cnt FROM users", ())
        user_count = result["cnt"] if result else 0
        return {"status": "ok", "users_in_db": user_count, "version": "1.0.0"}
    except Exception as e:
        return {"status": "db_error", "error": str(e)}


@app.get("/api/users-summary")
def users_summary():
    """Quick summary of all users with health score — for the user selector dropdown."""
    from src.db import fetch_all
    rows = fetch_all("""
        SELECT u.user_id, u.name, u.age, u.city, u.occupation, u.marital_status,
               fp.monthly_income, fp.risk_profile,
               mhs.overall_score, mhs.grade
        FROM users u
        LEFT JOIN financial_profiles fp ON fp.user_id = u.user_id
        LEFT JOIN money_health_scores mhs ON mhs.user_id = u.user_id
        ORDER BY u.user_id
    """, ())
    return rows


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("backend.main:app", host="0.0.0.0", port=port, reload=True)
