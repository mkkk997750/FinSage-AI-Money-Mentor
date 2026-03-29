"""
PostgreSQL Database Connection for FinSage
Provides a context-managed connection pool and helper functions.
"""
from __future__ import annotations

import os
from contextlib import contextmanager
from typing import Any

import psycopg2
import psycopg2.extras
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host":     os.getenv("PG_HOST",     "localhost"),
    "port":     int(os.getenv("PG_PORT", "5432")),
    "dbname":   os.getenv("PG_DB",       "finsage"),
    "user":     os.getenv("PG_USER",     "postgres"),
    "password": os.getenv("PG_PASSWORD", "postgres"),
}


def get_connection():
    """Return a new psycopg2 connection."""
    return psycopg2.connect(**DB_CONFIG)


@contextmanager
def db_cursor(cursor_factory=psycopg2.extras.RealDictCursor):
    """Context manager yielding a dict cursor; commits/rolls back automatically."""
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=cursor_factory) as cur:
            yield cur
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def fetch_all(sql: str, params: tuple = ()) -> list[dict]:
    with db_cursor() as cur:
        cur.execute(sql, params)
        return [dict(row) for row in cur.fetchall()]


def fetch_one(sql: str, params: tuple = ()) -> dict | None:
    with db_cursor() as cur:
        cur.execute(sql, params)
        row = cur.fetchone()
        return dict(row) if row else None


def execute(sql: str, params: tuple = ()) -> None:
    with db_cursor() as cur:
        cur.execute(sql, params)


def insert_returning(sql: str, params: tuple = ()) -> Any:
    """Execute an INSERT … RETURNING and return the first column of the first row."""
    with db_cursor() as cur:
        cur.execute(sql, params)
        row = cur.fetchone()
        return list(row.values())[0] if row else None


# ─── Domain helpers ──────────────────────────────────────────────────────────

def get_user_full_profile(user_id: int) -> dict | None:
    """Return user + financial_profile merged as a single dict."""
    row = fetch_one("""
        SELECT u.*, fp.monthly_income, fp.monthly_expenses, fp.monthly_savings,
               fp.emergency_fund, fp.pf_balance, fp.ppf_balance, fp.fd_balance,
               fp.stock_portfolio, fp.mf_portfolio_value, fp.real_estate_value,
               fp.gold_value, fp.nps_balance,
               fp.home_loan_outstanding, fp.car_loan_outstanding,
               fp.personal_loan_outstanding, fp.credit_card_outstanding,
               fp.monthly_emi, fp.existing_life_cover, fp.existing_health_cover,
               fp.retirement_age, fp.risk_profile
        FROM users u
        JOIN financial_profiles fp ON fp.user_id = u.user_id
        WHERE u.user_id = %s
    """, (user_id,))
    return row


def get_user_mf_holdings(user_id: int) -> list[dict]:
    return fetch_all(
        "SELECT * FROM mutual_fund_holdings WHERE user_id = %s ORDER BY current_value DESC",
        (user_id,)
    )


def get_user_goals(user_id: int) -> list[dict]:
    return fetch_all(
        "SELECT * FROM financial_goals WHERE user_id = %s ORDER BY priority, target_year",
        (user_id,)
    )


def get_user_tax_profile(user_id: int) -> dict | None:
    return fetch_one(
        "SELECT * FROM tax_profiles WHERE user_id = %s ORDER BY tax_id DESC LIMIT 1",
        (user_id,)
    )


def get_user_life_events(user_id: int) -> list[dict]:
    return fetch_all(
        "SELECT * FROM life_events WHERE user_id = %s ORDER BY event_date DESC",
        (user_id,)
    )


def get_user_insurance(user_id: int) -> list[dict]:
    return fetch_all(
        "SELECT * FROM insurance_policies WHERE user_id = %s AND is_active = true",
        (user_id,)
    )


def get_user_health_score(user_id: int) -> dict | None:
    return fetch_one(
        "SELECT * FROM money_health_scores WHERE user_id = %s ORDER BY computed_at DESC LIMIT 1",
        (user_id,)
    )


def save_health_score(user_id: int, score_data: dict) -> None:
    execute("""
        INSERT INTO money_health_scores
          (user_id, overall_score, grade, emergency_preparedness, insurance_coverage,
           investment_diversification, debt_health, tax_efficiency, retirement_readiness,
           strengths, weaknesses, top_recommendations)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT DO NOTHING
    """, (
        user_id,
        score_data.get("overall_score"),
        score_data.get("grade"),
        score_data.get("scores", {}).get("emergency_preparedness"),
        score_data.get("scores", {}).get("insurance_coverage"),
        score_data.get("scores", {}).get("investment_diversification"),
        score_data.get("scores", {}).get("debt_health"),
        score_data.get("scores", {}).get("tax_efficiency"),
        score_data.get("scores", {}).get("retirement_readiness"),
        ",".join(score_data.get("strengths", [])),
        ",".join(score_data.get("weaknesses", [])),
        "",
    ))


def save_session(session_id: str, user_id: int, agent_type: str) -> None:
    execute("""
        INSERT INTO agent_sessions (session_id, user_id, agent_type)
        VALUES (%s, %s, %s)
        ON CONFLICT (session_id) DO UPDATE SET last_active = NOW()
    """, (session_id, user_id, agent_type))


def save_message(session_id: str, role: str, content: str, agent_node: str = "") -> None:
    execute("""
        INSERT INTO conversation_history (session_id, role, content, agent_node)
        VALUES (%s, %s, %s, %s)
    """, (session_id, role, content, agent_node))


def get_session_history(session_id: str) -> list[dict]:
    return fetch_all(
        "SELECT * FROM conversation_history WHERE session_id = %s ORDER BY created_at",
        (session_id,)
    )
