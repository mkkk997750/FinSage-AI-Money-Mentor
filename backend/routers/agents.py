"""
Agent Execution Router — runs individual LangGraph agents via REST API
"""
from __future__ import annotations

import uuid
from typing import Any

from fastapi import APIRouter, HTTPException

from models import (
    AgentRequest,
    CouplePlanRequest,
    LifeEventRequest,
    MFXrayRequest,
    ChatRequest,
)
from src.db import (
    get_user_full_profile,
    get_user_mf_holdings,
    get_user_goals,
    get_user_tax_profile,
    get_user_life_events,
    get_user_insurance,
    get_user_health_score,
    save_session,
    save_message,
    get_session_history,
)
from src.nodes import (
    fire_planner_node,
    health_scorer_node,
    insurance_auditor_node,
    life_event_advisor_node,
    couple_planner_node,
    mf_xray_node,
    tax_optimizer_node,
    report_generator_node,
    profile_collector_node,
)

router = APIRouter(prefix="/api/agents", tags=["agents"])


def _build_profile(user_id: int) -> dict:
    """Merge DB data into a unified profile dict for LangGraph nodes."""
    row = get_user_full_profile(user_id)
    if not row:
        raise HTTPException(404, f"User {user_id} not found")
    goals = get_user_goals(user_id)
    insurance = get_user_insurance(user_id)
    profile = dict(row)
    profile["life_goals"] = [
        {
            "name": g["goal_name"],
            "amount": float(g["target_amount"] or 0),
            "years": max(1, int(g["target_year"] or 2035) - 2026),
        }
        for g in goals
    ]
    profile["insurance_policies"] = [
        {
            "type": p["policy_type"].replace("term_life", "term"),
            "cover": float(p["sum_assured"] or 0),
            "premium": float(p["annual_premium"] or 0),
            "insurer": p["insurer_name"],
        }
        for p in insurance
    ]
    profile["outstanding_loans"] = []
    if float(profile.get("home_loan_outstanding") or 0) > 0:
        profile["outstanding_loans"].append({
            "type": "home", "balance": float(profile["home_loan_outstanding"]),
            "emi": float(profile["monthly_emi"] or 0) * 0.6,
            "annual_interest": float(profile["home_loan_outstanding"]) * 0.085,
        })
    if float(profile.get("car_loan_outstanding") or 0) > 0:
        profile["outstanding_loans"].append({
            "type": "car", "balance": float(profile["car_loan_outstanding"]),
            "emi": float(profile["monthly_emi"] or 0) * 0.3,
        })
    if float(profile.get("personal_loan_outstanding") or 0) > 0:
        profile["outstanding_loans"].append({
            "type": "personal", "balance": float(profile["personal_loan_outstanding"]),
            "emi": float(profile["monthly_emi"] or 0) * 0.1,
        })
    profile["existing_savings"] = (
        float(profile.get("pf_balance") or 0) +
        float(profile.get("ppf_balance") or 0) +
        float(profile.get("fd_balance") or 0) +
        float(profile.get("nps_balance") or 0)
    )
    profile["equity_investments"] = (
        float(profile.get("stock_portfolio") or 0) +
        float(profile.get("mf_portfolio_value") or 0)
    )
    profile["annual_income"] = float(profile.get("monthly_income") or 0) * 12
    return profile


def _make_state(profile: dict, tasks: list[str] | None = None) -> dict:
    return {
        "messages": [],
        "user_profile": profile,
        "profile_complete": True,
        "tasks_requested": tasks or ["fire", "tax", "insurance"],
        "tasks_completed": [],
        "iteration": 0,
        "human_approved": False,
    }


def _extract_messages(state: dict) -> list[dict]:
    msgs = []
    for m in state.get("messages", []):
        role = getattr(m, "type", "assistant")
        # Patch: Map 'ai' role to 'assistant' for DB constraint
        if role == "ai":
            role = "assistant"
        content = getattr(m, "content", str(m))
        msgs.append({"role": role, "content": content})
    return msgs


# ─── Individual Agent Endpoints ───────────────────────────────────────────────

@router.post("/health-score")
def run_health_score(req: AgentRequest):
    session_id = req.session_id or str(uuid.uuid4())
    profile = _build_profile(req.user_id)
    save_session(session_id, req.user_id, "health_score")
    if req.message:
        save_message(session_id, "user", req.message)

    state = _make_state(profile)
    profile_state = profile_collector_node(state)
    state.update(profile_state)
    result_state = health_scorer_node(state)

    msgs = _extract_messages(result_state)
    for m in msgs:
        # Patch: Map 'ai' role to 'assistant' for DB constraint
        role = m["role"]
        if role == "ai":
            role = "assistant"
        save_message(session_id, role, m["content"], "health_scorer")

    return {
        "session_id": session_id,
        "agent_type": "health_score",
        "messages": msgs,
        "result": result_state.get("health_score_result"),
        "status": "success",
    }


@router.post("/fire-planner")
def run_fire_planner(req: AgentRequest):
    session_id = req.session_id or str(uuid.uuid4())
    profile = _build_profile(req.user_id)
    save_session(session_id, req.user_id, "fire_planner")
    if req.message:
        save_message(session_id, "user", req.message)

    state = _make_state(profile)
    result_state = fire_planner_node(state)

    msgs = _extract_messages(result_state)
    for m in msgs:
        # Patch: Map 'ai' role to 'assistant' for DB constraint
        role = m["role"]
        if role == "ai":
            role = "assistant"
        save_message(session_id, role, m["content"], "fire_planner")

    return {
        "session_id": session_id,
        "agent_type": "fire_planner",
        "messages": msgs,
        "result": result_state.get("fire_plan_result"),
        "status": "success",
    }


@router.post("/tax-wizard")
def run_tax_wizard(req: AgentRequest):
    session_id = req.session_id or str(uuid.uuid4())
    profile = _build_profile(req.user_id)
    save_session(session_id, req.user_id, "tax_wizard")
    if req.message:
        save_message(session_id, "user", req.message)

    state = _make_state(profile)
    result_state = tax_optimizer_node(state)

    msgs = _extract_messages(result_state)
    for m in msgs:
        # Patch: Map 'ai' role to 'assistant' for DB constraint
        role = m["role"]
        if role == "ai":
            role = "assistant"
        save_message(session_id, role, m["content"], "tax_optimizer")

    return {
        "session_id": session_id,
        "agent_type": "tax_wizard",
        "messages": msgs,
        "result": result_state.get("tax_analysis_result"),
        "status": "success",
    }


@router.post("/insurance-audit")
def run_insurance_audit(req: AgentRequest):
    session_id = req.session_id or str(uuid.uuid4())
    profile = _build_profile(req.user_id)
    save_session(session_id, req.user_id, "insurance_audit")
    if req.message:
        save_message(session_id, "user", req.message)

    state = _make_state(profile)
    result_state = insurance_auditor_node(state)

    msgs = _extract_messages(result_state)
    for m in msgs:
        # Patch: Map 'ai' role to 'assistant' for DB constraint
        role = m["role"]
        if role == "ai":
            role = "assistant"
        save_message(session_id, role, m["content"], "insurance_auditor")

    return {
        "session_id": session_id,
        "agent_type": "insurance_audit",
        "messages": msgs,
        "result": result_state.get("insurance_analysis_result"),
        "status": "success",
    }


@router.post("/life-event")
def run_life_event(req: LifeEventRequest):
    session_id = req.session_id or str(uuid.uuid4())
    profile = _build_profile(req.user_id)
    save_session(session_id, req.user_id, "life_event")
    save_message(session_id, "user", f"Life event: {req.event_type} - {req.description}")

    state = _make_state(profile, tasks=["life_event"])
    state["life_event_data"] = {
        "event_type": req.event_type,
        "amount_involved": req.amount_involved,
        "description": req.description,
    }
    result_state = life_event_advisor_node(state)

    msgs = _extract_messages(result_state)
    for m in msgs:
        # Patch: Map 'ai' role to 'assistant' for DB constraint
        role = m["role"]
        if role == "ai":
            role = "assistant"
        save_message(session_id, role, m["content"], "life_event_advisor")

    return {
        "session_id": session_id,
        "agent_type": "life_event",
        "messages": msgs,
        "result": result_state.get("life_event_result"),
        "status": "success",
    }


@router.post("/couple-planner")
def run_couple_planner(req: CouplePlanRequest):
    session_id = req.session_id or str(uuid.uuid4())
    profile1 = _build_profile(req.user1_id)
    profile2 = _build_profile(req.user2_id)
    save_session(session_id, req.user1_id, "couple_planner")
    save_message(session_id, "user", f"Couple planning for users {req.user1_id} and {req.user2_id}")

    state = _make_state(profile1, tasks=["couple"])
    state["couple_data"] = profile2
    result_state = couple_planner_node(state)

    msgs = _extract_messages(result_state)
    for m in msgs:
        # Patch: Map 'ai' role to 'assistant' for DB constraint
        role = m["role"]
        if role == "ai":
            role = "assistant"
        save_message(session_id, role, m["content"], "couple_planner")

    return {
        "session_id": session_id,
        "agent_type": "couple_planner",
        "messages": msgs,
        "result": result_state.get("couple_plan_result"),
        "status": "success",
    }


@router.post("/mf-xray")
def run_mf_xray(req: MFXrayRequest):
    session_id = req.session_id or str(uuid.uuid4())
    profile = _build_profile(req.user_id)
    holdings = get_user_mf_holdings(req.user_id)
    save_session(session_id, req.user_id, "mf_xray")
    save_message(session_id, "user", "MF Portfolio X-Ray analysis requested")

    state = _make_state(profile, tasks=["mf_xray"])
    state["mf_holdings"] = [dict(h) for h in holdings]
    result_state = mf_xray_node(state)

    msgs = _extract_messages(result_state)
    for m in msgs:
        # Patch: Map 'ai' role to 'assistant' for DB constraint
        role = m["role"]
        if role == "ai":
            role = "assistant"
        save_message(session_id, role, m["content"], "mf_xray")

    return {
        "session_id": session_id,
        "agent_type": "mf_xray",
        "messages": msgs,
        "result": result_state.get("mf_xray_result"),
        "status": "success",
    }


@router.post("/full-analysis")
def run_full_analysis(req: AgentRequest):
    """Run all agents via the complete LangGraph graph (no HITL)."""
    from src.graph import build_graph
    session_id = req.session_id or str(uuid.uuid4())
    profile = _build_profile(req.user_id)
    save_session(session_id, req.user_id, "full_analysis")
    if req.message:
        save_message(session_id, "user", req.message)

    graph = build_graph(use_hitl=False)
    tasks = req.tasks_requested or ["fire", "tax", "insurance"]
    initial_state = {
        "messages": [],
        "user_profile": profile,
        "profile_complete": False,
        "tasks_requested": tasks,
        "tasks_completed": [],
        "iteration": 0,
        "human_approved": False,
        "human_feedback": "yes",
    }

    config = {"configurable": {"thread_id": session_id}}
    final_state: dict[str, Any] = {}
    all_messages: list[dict] = []

    for chunk in graph.stream(initial_state, config):
        for node_name, node_output in chunk.items():
            final_state.update(node_output)
            for msg in node_output.get("messages", []):
                content = getattr(msg, "content", str(msg))
                role = getattr(msg, "type", "assistant")
                all_messages.append({"role": role, "content": content, "node": node_name})
                # Patch: Map 'ai' role to 'assistant' for DB constraint
                db_role = role
                if db_role == "ai":
                    db_role = "assistant"
                save_message(session_id, db_role, content, node_name)

    return {
        "session_id": session_id,
        "agent_type": "full_analysis",
        "messages": all_messages,
        "result": {
            "health_score": final_state.get("health_score_result"),
            "fire_plan": final_state.get("fire_plan_result"),
            "tax_analysis": final_state.get("tax_analysis_result"),
            "insurance": final_state.get("insurance_analysis_result"),
            "final_report": final_state.get("final_report"),
        },
        "status": "success",
    }


@router.get("/sessions/{session_id}/history")
def get_chat_history(session_id: str):
    return get_session_history(session_id)
