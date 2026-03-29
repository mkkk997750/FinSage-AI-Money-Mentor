"""
Data Browser Router — exposes all DB tables as paginated JSON APIs
"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from src.db import fetch_all, fetch_one

router = APIRouter(prefix="/api/data", tags=["data"])


def _table_query(table: str, user_id: int | None, limit: int, offset: int) -> list[dict]:
    where = f"WHERE user_id = {user_id}" if user_id else ""
    return fetch_all(
        f"SELECT * FROM {table} {where} ORDER BY 1 LIMIT %s OFFSET %s",
        (limit, offset),
    )


@router.get("/users")
def list_users(limit: int = Query(50, le=200), offset: int = 0):
    return fetch_all("SELECT * FROM users ORDER BY user_id LIMIT %s OFFSET %s", (limit, offset))


@router.get("/users/{user_id}")
def get_user(user_id: int):
    row = fetch_one("SELECT * FROM users WHERE user_id = %s", (user_id,))
    if not row:
        raise HTTPException(404, "User not found")
    return row


@router.get("/financial-profiles")
def list_financial_profiles(user_id: int = None, limit: int = 50, offset: int = 0):
    return _table_query("financial_profiles", user_id, limit, offset)


@router.get("/financial-goals")
def list_financial_goals(user_id: int = None, limit: int = 100, offset: int = 0):
    return _table_query("financial_goals", user_id, limit, offset)


@router.get("/mutual-funds")
def list_mutual_funds(user_id: int = None, limit: int = 100, offset: int = 0):
    return _table_query("mutual_fund_holdings", user_id, limit, offset)


@router.get("/tax-profiles")
def list_tax_profiles(user_id: int = None, limit: int = 50, offset: int = 0):
    return _table_query("tax_profiles", user_id, limit, offset)


@router.get("/life-events")
def list_life_events(user_id: int = None, limit: int = 100, offset: int = 0):
    return _table_query("life_events", user_id, limit, offset)


@router.get("/insurance")
def list_insurance(user_id: int = None, limit: int = 100, offset: int = 0):
    return _table_query("insurance_policies", user_id, limit, offset)


@router.get("/couple-profiles")
def list_couple_profiles(limit: int = 20, offset: int = 0):
    return fetch_all(
        """SELECT cp.*, u1.name as partner1_name, u2.name as partner2_name
           FROM couple_profiles cp
           JOIN users u1 ON u1.user_id = cp.partner1_user_id
           JOIN users u2 ON u2.user_id = cp.partner2_user_id
           ORDER BY cp.couple_id LIMIT %s OFFSET %s""",
        (limit, offset),
    )


@router.get("/health-scores")
def list_health_scores(user_id: int = None, limit: int = 50, offset: int = 0):
    return _table_query("money_health_scores", user_id, limit, offset)


@router.get("/sessions")
def list_sessions(user_id: int = None, limit: int = 50, offset: int = 0):
    where = f"WHERE user_id = {user_id}" if user_id else ""
    return fetch_all(
        f"SELECT * FROM agent_sessions {where} ORDER BY last_active DESC LIMIT %s OFFSET %s",
        (limit, offset),
    )


@router.get("/sessions/{session_id}/history")
def get_session_history(session_id: str):
    return fetch_all(
        "SELECT * FROM conversation_history WHERE session_id = %s ORDER BY created_at",
        (session_id,),
    )


@router.get("/dashboard/{user_id}")
def get_dashboard_data(user_id: int):
    """Return all data for a user's dashboard in a single call."""
    profile  = fetch_one(
        "SELECT u.*, fp.* FROM users u JOIN financial_profiles fp ON fp.user_id = u.user_id WHERE u.user_id = %s",
        (user_id,),
    )
    if not profile:
        raise HTTPException(404, "User not found")
    goals    = fetch_all("SELECT * FROM financial_goals WHERE user_id = %s", (user_id,))
    mf_funds = fetch_all("SELECT * FROM mutual_fund_holdings WHERE user_id = %s ORDER BY current_value DESC", (user_id,))
    tax      = fetch_one("SELECT * FROM tax_profiles WHERE user_id = %s LIMIT 1", (user_id,))
    events   = fetch_all("SELECT * FROM life_events WHERE user_id = %s", (user_id,))
    insurance= fetch_all("SELECT * FROM insurance_policies WHERE user_id = %s AND is_active = true", (user_id,))
    health   = fetch_one("SELECT * FROM money_health_scores WHERE user_id = %s ORDER BY computed_at DESC LIMIT 1", (user_id,))
    return {
        "profile":   profile,
        "goals":     goals,
        "mf_funds":  mf_funds,
        "tax":       tax,
        "events":    events,
        "insurance": insurance,
        "health":    health,
    }
