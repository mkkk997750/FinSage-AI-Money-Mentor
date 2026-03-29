"""
LangGraph Agent Node Functions for FinSage

Each function IS a LangGraph node:
  - Takes MoneyMentorState as input
  - Returns a dict with only the state keys it updates (partial update)
  - Uses financial_tools for deterministic calculations
  - Optionally calls the LLM for narrative / explanation

Nodes in this file:
  profile_collector_node   — validates / loads user profile
  health_scorer_node       — 6-dimension financial health score
  supervisor_node          — orchestration & status reporting
  fire_planner_node        — FIRE retirement roadmap
  tax_optimizer_node       — tax regime comparison & deductions
  insurance_auditor_node   — coverage gap detection
  report_generator_node    — synthesise everything into final plan
  human_review_node        — process human feedback (HITL)
"""
from __future__ import annotations

import json
from typing import Any

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from src.llm_config import get_llm
from src.state import MoneyMentorState
from src.tools import (
    calculate_financial_health_score,
    calculate_insurance_requirement,
    calculate_retirement_corpus,
    calculate_sip_required,
    calculate_tax_liability,
    suggest_asset_allocation,
)


# ─── Helpers ─────────────────────────────────────────────────────────────────

def _llm_narrative(prompt: str, fallback: str = "") -> str:
    """Call LLM for a narrative explanation; return fallback if LLM unavailable."""
    llm = get_llm()
    if not llm:
        return fallback
    try:
        return llm.invoke([HumanMessage(content=prompt)]).content
    except Exception as exc:
        return f"[LLM error: {exc}] {fallback}"


def _inr(amount: float) -> str:
    """Format as Indian Rupees."""
    if amount >= 1_00_00_000:
        return f"₹{amount/1_00_00_000:.2f} Cr"
    if amount >= 1_00_000:
        return f"₹{amount/1_00_000:.1f}L"
    return f"₹{amount:,.0f}"


def _grade_label(grade: str) -> str:
    return {
        "A": "Excellent 🌟",
        "B": "Good 👍",
        "C": "Average — room for improvement ⚡",
        "D": "Below average — needs attention ⚠️",
        "F": "Critical — immediate action required 🚨",
    }.get(grade, "Average")


# ─── Node 1: Profile Collector ────────────────────────────────────────────────

def profile_collector_node(state: MoneyMentorState) -> dict:
    """
    Validate that a user profile is loaded.

    In demo/app mode the profile is pre-loaded in the initial state.
    In full interactive mode (future extension) the LLM would conduct a
    profiling conversation — the messages list accumulates those turns.
    """
    profile = state.get("user_profile")

    required_keys = [
        "age", "monthly_income", "monthly_expenses",
        "retirement_age", "risk_profile",
    ]

    if profile and all(profile.get(k) for k in required_keys):
        greet = AIMessage(content=(
            f"## 👋 Welcome to FinSage, {profile.get('name', 'valued user')}!\n\n"
            f"I've loaded your financial profile. Here's a quick summary:\n"
            f"- **Age:** {profile['age']} | **Retirement target:** {profile.get('retirement_age', 60)}\n"
            f"- **Monthly income:** {_inr(profile['monthly_income'])} | "
            f"**Expenses:** {_inr(profile['monthly_expenses'])}\n"
            f"- **Risk profile:** {profile.get('risk_profile', 'moderate').capitalize()}\n"
            f"- **Existing savings:** {_inr(profile.get('existing_savings', 0))}\n\n"
            f"Starting your comprehensive financial analysis now... 🚀"
        ))
        return {
            "profile_complete": True,
            "messages": [greet],
            "tasks_requested": ["fire", "tax", "insurance"],
            "tasks_completed": [],
            "iteration": 0,
            "human_approved": False,
        }

    # Profile missing or incomplete
    msg = AIMessage(content=(
        "❗ No complete financial profile found. "
        "Please provide your profile data to proceed.\n"
        "Run `demo.py` to see a full example with a sample profile."
    ))
    return {"profile_complete": False, "messages": [msg]}


# ─── Node 2: Financial Health Scorer ─────────────────────────────────────────

def health_scorer_node(state: MoneyMentorState) -> dict:
    """
    LangGraph Node: Calculate the 6-dimension financial health score.

    Directly invokes the @tool `calculate_financial_health_score`.
    Optionally calls the LLM for a personalised commentary.
    """
    profile = state["user_profile"]

    total_emi = sum(
        loan.get("emi", 0) for loan in profile.get("outstanding_loans", [])
    )
    life_cover = sum(
        p.get("cover", 0)
        for p in profile.get("insurance_policies", [])
        if p.get("type") in ("term", "life")
    )
    health_cover = sum(
        p.get("cover", 0)
        for p in profile.get("insurance_policies", [])
        if p.get("type") == "health"
    )

    result = calculate_financial_health_score.invoke({
        "monthly_income": profile["monthly_income"],
        "monthly_expenses": profile["monthly_expenses"],
        "emergency_fund": profile.get("emergency_fund", 0),
        "total_debt_emi": total_emi,
        "total_savings": profile.get("existing_savings", 0),
        "life_cover": life_cover,
        "health_cover": health_cover,
        "age": profile["age"],
    })

    scores = result["scores"]
    dim_lines = "\n".join(
        f"  - {k.replace('_', ' ').title()}: **{v}/100**"
        for k, v in scores.items()
    )

    # Optional LLM commentary
    llm_comment = _llm_narrative(
        prompt=(
            f"In 2 sentences, give a financial advisor's reaction to this health score for "
            f"a {profile['age']}-year-old earning {_inr(profile['monthly_income'])}/month. "
            f"Score: {result['overall_score']}/100 (Grade {result['grade']}). "
            f"Weaknesses: {result['weaknesses']}. Be concise and encouraging."
        ),
        fallback=(
            f"Your score of {result['overall_score']}/100 "
            f"({'focus on ' + ', '.join(result['weaknesses']) if result['weaknesses'] else 'keep up the great work'})."
        ),
    )

    message = AIMessage(content=(
        f"## 📊 Financial Health Score\n\n"
        f"**Overall: {result['overall_score']}/100 — {_grade_label(result['grade'])}**\n\n"
        f"**Dimension Breakdown:**\n{dim_lines}\n\n"
        f"**Strengths:** {', '.join(result['strengths']) or 'None yet'}\n"
        f"**Improve:** {', '.join(result['weaknesses']) or 'All good!'}\n\n"
        f"> {llm_comment}"
    ))

    return {
        "health_score_result": result,
        "messages": [message],
    }


# ─── Node 3: Supervisor ───────────────────────────────────────────────────────

def supervisor_node(state: MoneyMentorState) -> dict:
    """
    Supervisor Agent — orchestrates specialised agents.

    Reads tasks_requested and tasks_completed to determine what remains.
    Routes are defined in graph.py via conditional edges (supervisor_router).
    This node itself just logs the orchestration decision.
    """
    requested = set(state.get("tasks_requested", []))
    completed = set(state.get("tasks_completed", []))
    remaining = requested - completed
    iteration = state.get("iteration", 0) + 1

    next_task = next(
        (t for t in ("fire", "tax", "insurance") if t in remaining),
        "report_generator",
    )

    agent_names = {
        "fire": "🔥 FIRE Path Planner",
        "tax": "💰 Tax Optimizer",
        "insurance": "🛡️ Insurance Auditor",
        "report_generator": "📋 Report Generator",
    }

    msg = AIMessage(content=(
        f"### 🎯 Supervisor — Iteration {iteration}\n"
        f"- Completed: {sorted(completed) or '—'}\n"
        f"- Remaining: {sorted(remaining) or '—'}\n"
        f"- Dispatching → **{agent_names.get(next_task, next_task)}**"
    ))

    return {"messages": [msg], "iteration": iteration}


# ─── Node 4: FIRE Planner ─────────────────────────────────────────────────────

def fire_planner_node(state: MoneyMentorState) -> dict:
    """
    FIRE Path Planner Agent

    Demonstrates chaining multiple @tool calls inside a single LangGraph node:
      1. calculate_retirement_corpus   → how much is needed
      2. calculate_sip_required        → monthly SIP to reach corpus
      3. suggest_asset_allocation      → recommended portfolio split
      4. calculate_sip_required (×N)   → per-goal SIP breakdown

    Optionally calls LLM for a personalised narrative.
    """
    profile = state["user_profile"]

    # ── Tool calls ──────────────────────────────────────────────────────────
    corpus_data = calculate_retirement_corpus.invoke({
        "current_monthly_expenses": profile["monthly_expenses"],
        "current_age": profile["age"],
        "retirement_age": profile.get("retirement_age", 60),
        "life_expectancy": 85,
        "inflation_rate": 6.0,
        "post_retirement_return": 7.0,
    })

    existing = profile.get("existing_savings", 0) + profile.get("equity_investments", 0)
    sip_data = calculate_sip_required.invoke({
        "corpus_needed": corpus_data["corpus_required"],
        "years": corpus_data["years_to_retirement"],
        "expected_return_rate": 12.0,
        "existing_corpus": existing,
    })

    allocation_data = suggest_asset_allocation.invoke({
        "age": profile["age"],
        "risk_profile": profile.get("risk_profile", "moderate"),
    })

    # Goal-wise SIP breakdown
    goal_sips: list[dict] = []
    for goal in profile.get("life_goals", []):
        g_sip = calculate_sip_required.invoke({
            "corpus_needed": goal.get("amount", 0),
            "years": goal.get("years", 10),
            "expected_return_rate": 10.0,
            "existing_corpus": 0,
        })
        goal_sips.append({
            "goal_name": goal.get("name", "Goal"),
            "target_amount": goal.get("amount", 0),
            "years": goal.get("years", 10),
            "monthly_sip_required": g_sip["monthly_sip"],
        })

    total_goal_sip = sum(g["monthly_sip_required"] for g in goal_sips)
    total_sip = sip_data["monthly_sip"] + total_goal_sip

    fire_plan = {
        "corpus_required": corpus_data["corpus_required"],
        "corpus_in_crores": corpus_data["corpus_in_crores"],
        "years_to_retirement": corpus_data["years_to_retirement"],
        "monthly_expenses_at_retirement": corpus_data["monthly_expenses_at_retirement"],
        "existing_corpus": existing,
        "retirement_sip": sip_data["monthly_sip"],
        "goal_sips": goal_sips,
        "total_monthly_sip": total_sip,
        "asset_allocation": allocation_data,
        "wealth_created": sip_data["wealth_created"],
    }

    # ── LLM narrative ───────────────────────────────────────────────────────
    alloc = allocation_data
    narrative = _llm_narrative(
        prompt=(
            f"You are a SEBI-registered financial planner. Write 3 short encouraging "
            f"sentences about this FIRE plan for a {profile['age']}-year-old "
            f"earning {_inr(profile['monthly_income'])}/month:\n"
            f"- Corpus needed: {_inr(corpus_data['corpus_required'])}\n"
            f"- Years to retire: {corpus_data['years_to_retirement']}\n"
            f"- Monthly SIP needed: {_inr(total_sip)}\n"
            f"Keep it specific and actionable."
        ),
        fallback=(
            f"You need to invest {_inr(total_sip)}/month to retire in "
            f"{corpus_data['years_to_retirement']} years with a corpus of "
            f"{_inr(corpus_data['corpus_required'])}."
        ),
    )
    fire_plan["narrative"] = narrative

    # ── Goal table ──────────────────────────────────────────────────────────
    goal_rows = "\n".join(
        f"  | {g['goal_name'].replace('_', ' ').title()} | "
        f"{_inr(g['target_amount'])} | {g['years']}y | {_inr(g['monthly_sip_required'])}/mo |"
        for g in goal_sips
    ) or "  | — | — | — | — |"

    msg = AIMessage(content=(
        f"## 🔥 FIRE Path Planner — Retirement Roadmap\n\n"
        f"| Metric | Value |\n|---|---|\n"
        f"| Retirement Corpus Needed | **{_inr(corpus_data['corpus_required'])}** |\n"
        f"| Years to Retirement | **{corpus_data['years_to_retirement']} years** |\n"
        f"| Monthly Expenses at Retirement | {_inr(corpus_data['monthly_expenses_at_retirement'])} |\n"
        f"| Existing Corpus | {_inr(existing)} |\n"
        f"| Retirement SIP Required | **{_inr(sip_data['monthly_sip'])}/month** |\n\n"
        f"**Life Goal SIPs:**\n"
        f"  | Goal | Amount | Timeline | SIP |\n  |---|---|---|---|\n{goal_rows}\n\n"
        f"**Total Monthly SIP: {_inr(total_sip)}/month** "
        f"({round(total_sip/profile['monthly_income']*100, 1)}% of income)\n\n"
        f"**Suggested Allocation:** Equity {alloc['equity_pct']}% | "
        f"Debt {alloc['debt_pct']}% | Gold {alloc['gold_pct']}%\n\n"
        f"> {narrative}"
    ))

    tasks_completed = list(state.get("tasks_completed", [])) + ["fire"]
    return {
        "fire_plan_result": fire_plan,
        "tasks_completed": tasks_completed,
        "current_agent": "fire_planner",
        "messages": [msg],
    }


# ─── Node 5: Tax Optimizer ────────────────────────────────────────────────────

def tax_optimizer_node(state: MoneyMentorState) -> dict:
    """
    Tax Wizard Agent

    Demonstrates conditional tool invocation and comparison logic:
      - Runs calculate_tax_liability for BOTH old and new regime
      - Compares results and recommends the better regime
      - Identifies deductions the user is not yet claiming
    """
    profile = state["user_profile"]
    annual_income = profile.get("annual_income", profile["monthly_income"] * 12)

    # Build deductions dict from profile
    deductions: dict[str, float] = {}
    savings = profile.get("existing_savings", 0)
    if savings > 0:
        deductions["80C"] = min(float(savings), 150_000)

    home_loan = next(
        (l for l in profile.get("outstanding_loans", []) if l.get("type") == "home"),
        None,
    )
    if home_loan:
        deductions["home_loan_interest"] = float(
            min(home_loan.get("annual_interest", 0), 200_000)
        )

    health_ins = next(
        (p for p in profile.get("insurance_policies", []) if p.get("type") == "health"),
        None,
    )
    if health_ins:
        deductions["80D"] = float(min(health_ins.get("premium", 0), 25_000))

    # ── Tool calls ──────────────────────────────────────────────────────────
    old_tax = calculate_tax_liability.invoke({
        "annual_income": annual_income,
        "deductions": deductions,
        "regime": "old",
    })
    new_tax = calculate_tax_liability.invoke({
        "annual_income": annual_income,
        "deductions": {},
        "regime": "new",
    })

    recommended = "new" if new_tax["total_tax"] <= old_tax["total_tax"] else "old"
    savings_amount = abs(old_tax["total_tax"] - new_tax["total_tax"])

    # Identify missed deductions (old regime only)
    missed: dict[str, Any] = {}
    if recommended == "old":
        if deductions.get("80C", 0) < 150_000:
            missed["80C_remaining_limit"] = 150_000 - deductions.get("80C", 0)
        missed["NPS_80CCD_1B"] = 50_000  # additional NPS benefit
        missed["health_insurance_80D"] = 25_000 if "80D" not in deductions else 0

    tax_analysis = {
        "annual_income": annual_income,
        "old_regime_tax": old_tax["total_tax"],
        "new_regime_tax": new_tax["total_tax"],
        "recommended_regime": recommended,
        "annual_savings": savings_amount,
        "monthly_savings": round(savings_amount / 12),
        "deductions_claimed": deductions,
        "missed_deductions": {k: v for k, v in missed.items() if v > 0},
        "old_details": old_tax,
        "new_details": new_tax,
    }

    # ── LLM narrative ───────────────────────────────────────────────────────
    narrative = _llm_narrative(
        prompt=(
            f"In 2 sentences, explain why the {recommended} tax regime saves "
            f"{_inr(savings_amount)}/year for someone earning {_inr(annual_income)}/year. "
            f"Be specific and practical."
        ),
        fallback=(
            f"Switching to the {recommended.upper()} regime saves "
            f"{_inr(savings_amount)} ({_inr(round(savings_amount/12))}/month) annually."
        ),
    )

    missed_str = (
        "\n".join(f"  - {k}: {_inr(v)}" for k, v in missed.items() if v > 0)
        or "  None — good job!"
    )

    msg = AIMessage(content=(
        f"## 💰 Tax Analysis & Optimization\n\n"
        f"| Regime | Taxable Income | Annual Tax | Effective Rate |\n|---|---|---|---|\n"
        f"| Old | {_inr(old_tax['taxable_income'])} | {_inr(old_tax['total_tax'])} | "
        f"{old_tax['effective_rate_pct']}% |\n"
        f"| New | {_inr(new_tax['taxable_income'])} | {_inr(new_tax['total_tax'])} | "
        f"{new_tax['effective_rate_pct']}% |\n\n"
        f"**✅ Recommended: {recommended.upper()} REGIME**\n"
        f"You save **{_inr(savings_amount)}/year** ({_inr(round(savings_amount/12))}/month)\n\n"
        f"**Missed deductions (if you switch to old regime):**\n{missed_str}\n\n"
        f"> {narrative}"
    ))

    tasks_completed = list(state.get("tasks_completed", [])) + ["tax"]
    return {
        "tax_analysis_result": tax_analysis,
        "tasks_completed": tasks_completed,
        "current_agent": "tax_optimizer",
        "messages": [msg],
    }


# ─── Node 6: Insurance Auditor ────────────────────────────────────────────────

def insurance_auditor_node(state: MoneyMentorState) -> dict:
    """
    Insurance Auditor Agent

    Uses calculate_insurance_requirement tool to identify coverage gaps
    and generate actionable recommendations.
    """
    profile = state["user_profile"]

    current_life = sum(
        p.get("cover", 0)
        for p in profile.get("insurance_policies", [])
        if p.get("type") in ("term", "life")
    )
    current_health = sum(
        p.get("cover", 0)
        for p in profile.get("insurance_policies", [])
        if p.get("type") == "health"
    )
    dependents = profile.get("dependents", 2)

    result = calculate_insurance_requirement.invoke({
        "monthly_income": profile["monthly_income"],
        "age": profile["age"],
        "dependents": dependents,
        "existing_life_cover": float(current_life),
        "existing_health_cover": float(current_health),
    })

    recommendations: list[str] = []
    if result["life_cover_gap"] > 0:
        recommendations.append(
            f"Buy ₹{result['life_cover_gap_cr']:.1f} Cr term plan "
            f"(~₹{result['estimated_term_premium_pa']:,}/year)"
        )
    if result["health_cover_gap"] > 0:
        recommendations.append(
            f"Top up health cover by {_inr(result['health_cover_gap'])} "
            f"(~₹{result['estimated_health_premium_pa']:,}/year)"
        )
    if not any(p.get("type") == "accident" for p in profile.get("insurance_policies", [])):
        recommendations.append("Add Personal Accident cover of ₹50–100L (₹2,000–4,000/year)")
    if not any(p.get("type") == "critical_illness" for p in profile.get("insurance_policies", [])):
        recommendations.append("Consider Critical Illness rider ₹25–50L")

    insurance_analysis = {**result, "recommendations": recommendations}

    status = "✅ Adequately covered" if result["adequately_covered"] else "⚠️ Coverage gaps found"
    rec_str = "\n".join(f"- {r}" for r in recommendations) or "- No action needed."

    narrative = _llm_narrative(
        prompt=(
            f"In 2 sentences, explain the insurance gap for a {profile['age']}-year-old. "
            f"Life gap: {_inr(result['life_cover_gap'])}. "
            f"Health gap: {_inr(result['health_cover_gap'])}. Be direct and practical."
        ),
        fallback=f"Address the coverage gaps to protect your family's financial future.",
    )

    msg = AIMessage(content=(
        f"## 🛡️ Insurance Audit\n\n"
        f"| Type | Current | Recommended | Gap |\n|---|---|---|---|\n"
        f"| Life (Term) | {_inr(current_life)} | {_inr(result['recommended_life_cover'])} | "
        f"**{_inr(result['life_cover_gap'])}** |\n"
        f"| Health | {_inr(current_health)} | {_inr(result['recommended_health_cover'])} | "
        f"**{_inr(result['health_cover_gap'])}** |\n\n"
        f"**Status: {status}**\n\n"
        f"**Recommendations:**\n{rec_str}\n\n"
        f"**Additional annual premium needed:** {_inr(result['total_additional_premium_pa'])}\n\n"
        f"> {narrative}"
    ))

    tasks_completed = list(state.get("tasks_completed", [])) + ["insurance"]
    return {
        "insurance_analysis_result": insurance_analysis,
        "tasks_completed": tasks_completed,
        "current_agent": "insurance_auditor",
        "messages": [msg],
    }


# ─── Node 7: Report Generator ─────────────────────────────────────────────────

def report_generator_node(state: MoneyMentorState) -> dict:
    """
    Report Generator Agent — synthesises all analyses into a final plan.

    Reads results from all previous agents via state and composes
    a comprehensive, actionable financial plan document.
    """
    profile = state["user_profile"]
    health = state.get("health_score_result") or {}
    fire = state.get("fire_plan_result") or {}
    tax = state.get("tax_analysis_result") or {}
    ins = state.get("insurance_analysis_result") or {}

    sections: list[str] = []

    # Header
    sections.append(
        f"# 📊 FinSage — Your Personal Financial Plan\n\n"
        f"**Prepared for:** {profile.get('name', 'Valued User')}  "
        f"| **Age:** {profile['age']}  "
        f"| **Date:** 28 March 2026\n\n---\n"
    )

    # Executive Summary
    grade = health.get("grade", "C")
    weaknesses = health.get("weaknesses", [])
    sections.append(
        f"## 🎯 Executive Summary\n\n"
        f"**Financial Health Score:** {health.get('overall_score', 0):.0f}/100 "
        f"— {_grade_label(grade)}\n\n"
        f"| Dimension | Score |\n|---|---|\n"
        + "\n".join(
            f"| {k.replace('_', ' ').title()} | {v}/100 |"
            for k, v in health.get("scores", {}).items()
        )
        + f"\n\n"
        f"**Key areas to improve:** "
        f"{', '.join(weaknesses) or 'None — excellent foundations!'}\n\n---\n"
    )

    # FIRE Plan
    if fire:
        alloc = fire.get("asset_allocation", {})
        goal_rows = "\n".join(
            f"| {g['goal_name'].replace('_',' ').title()} | "
            f"{_inr(g['target_amount'])} | {g['years']}y | {_inr(g['monthly_sip_required'])}/mo |"
            for g in fire.get("goal_sips", [])
        ) or "| — | — | — | — |"
        sections.append(
            f"## 🔥 Retirement & Goals (FIRE Plan)\n\n"
            f"- **Target Corpus:** {_inr(fire.get('corpus_required', 0))} "
            f"({fire.get('corpus_in_crores', 0):.2f} Crores)\n"
            f"- **Years to Retirement:** {fire.get('years_to_retirement', 0)}\n"
            f"- **Monthly Expenses at Retirement:** "
            f"{_inr(fire.get('monthly_expenses_at_retirement', 0))}\n"
            f"- **Retirement SIP:** {_inr(fire.get('retirement_sip', 0))}/month\n"
            f"- **Total Monthly SIP (all goals):** {_inr(fire.get('total_monthly_sip', 0))}/month\n\n"
            f"**Life Goal Breakdown:**\n"
            f"| Goal | Target | Timeline | Monthly SIP |\n|---|---|---|---|\n{goal_rows}\n\n"
            f"**Recommended Portfolio Allocation:**\n"
            f"- Equity: {alloc.get('equity_pct', 60)}% "
            f"(Large {alloc.get('equity_breakdown',{}).get('large_cap_funds',0)}% | "
            f"Mid {alloc.get('equity_breakdown',{}).get('mid_cap_funds',0)}% | "
            f"Small {alloc.get('equity_breakdown',{}).get('small_cap_funds',0)}%)\n"
            f"- Debt: {alloc.get('debt_pct', 35)}% (PPF/EPF + Debt MFs + FDs)\n"
            f"- Gold: {alloc.get('gold_pct', 5)}% (Sovereign Gold Bonds)\n\n"
            f"{fire.get('narrative', '')}\n\n---\n"
        )

    # Tax Strategy
    if tax:
        rec = tax.get("recommended_regime", "new").upper()
        savings_pa = tax.get("annual_savings", 0)
        missed = tax.get("missed_deductions", {})
        missed_str = (
            "\n".join(f"  - {k}: {_inr(v)}" for k, v in missed.items())
            or "  None"
        )
        sections.append(
            f"## 💰 Tax Strategy\n\n"
            f"- **Recommended Regime:** {rec}\n"
            f"- **Annual Tax (recommended):** "
            f"{_inr(min(tax.get('old_regime_tax',0), tax.get('new_regime_tax',0)))}\n"
            f"- **Annual Savings vs Alternative:** {_inr(savings_pa)} "
            f"({_inr(round(savings_pa/12))}/month)\n"
            f"- **Effective Tax Rate:** "
            f"{tax.get('old_details' if rec=='OLD' else 'new_details', {}).get('effective_rate_pct', 0)}%\n\n"
            f"**Missed Deductions (to act on):**\n{missed_str}\n\n---\n"
        )

    # Insurance Plan
    if ins:
        recs = ins.get("recommendations", [])
        rec_str = "\n".join(f"- {r}" for r in recs) or "- Coverage is adequate."
        sections.append(
            f"## 🛡️ Insurance Coverage Plan\n\n"
            f"- **Life Cover:** current {_inr(ins.get('current_life_cover',0))} → "
            f"recommended {_inr(ins.get('recommended_life_cover',0))}\n"
            f"- **Health Cover:** current {_inr(ins.get('current_health_cover',0))} → "
            f"recommended {_inr(ins.get('recommended_health_cover',0))}\n"
            f"- **Status:** {'✅ Adequate' if ins.get('adequately_covered') else '⚠️ Gaps found'}\n"
            f"- **Additional premium needed:** {_inr(ins.get('total_additional_premium_pa',0))}/year\n\n"
            f"**Actions:**\n{rec_str}\n\n---\n"
        )

    # 30-Day Action Plan
    actions: list[str] = []
    if tax:
        actions.append(
            f"Inform payroll to apply {tax.get('recommended_regime','new').upper()} "
            f"tax regime immediately (saves {_inr(tax.get('monthly_savings',0))}/month)"
        )
    if fire:
        actions.append(
            f"Set up SIP of {_inr(fire.get('total_monthly_sip',0))}/month across equity MFs"
        )
    if ins and not ins.get("adequately_covered"):
        actions.append(
            f"Purchase additional insurance: {'; '.join(ins.get('recommendations',[])[:2])}"
        )
    monthly_exp = profile.get("monthly_expenses", 50000)
    ef = profile.get("emergency_fund", 0)
    ef_target = monthly_exp * 6
    if ef < ef_target:
        actions.append(
            f"Build emergency fund to {_inr(ef_target)} ({_inr(ef_target - ef)} more needed)"
        )
    actions.append("Review and rebalance portfolio every 6 months")

    action_str = "\n".join(f"{i+1}. {a}" for i, a in enumerate(actions))
    sections.append(f"## 📋 30-Day Action Plan\n\n{action_str}\n\n---\n")

    # LLM final insights
    llm_insights = _llm_narrative(
        prompt=(
            f"As a CFP, add 2-3 important financial insights or warnings for: "
            f"Age {profile['age']}, income {_inr(profile['monthly_income'])}/month, "
            f"health score {health.get('overall_score',0):.0f}/100, "
            f"corpus needed {_inr(fire.get('corpus_required',0))}. Be specific."
        ),
        fallback=(
            "Start investing early, maintain discipline with SIPs, "
            "and review your financial plan annually."
        ),
    )
    sections.append(
        f"## 🤖 AI Advisor Insights\n\n{llm_insights}\n\n"
        f"---\n*Generated by FinSage — AI Money Mentor | ET AI Hackathon 2026*\n"
    )

    final_report = "\n".join(sections)

    msg = AIMessage(content=final_report)
    return {
        "final_report": final_report,
        "messages": [msg],
        "current_agent": "report_generator",
    }


# ─── Node 8: Human Review (HITL) ─────────────────────────────────────────────

def human_review_node(state: MoneyMentorState) -> dict:
    """
    Human-in-the-Loop Review Node

    The graph is compiled with interrupt_before=["human_review"], which means
    LangGraph PAUSES before executing this node and waits for the caller to:
      1. Read the current state (final_report)
      2. Call graph.update_state(config, {"human_feedback": "yes/refine/..."})
      3. Resume with graph.stream(None, config)

    This node then routes:
      - "yes" / "approve" → END (plan accepted)
      - anything else     → back to supervisor for refinement
    """
    feedback = (state.get("human_feedback") or "").strip().lower()
    approved = feedback in ("", "yes", "y", "approve", "ok", "good", "looks good")

    if approved:
        confirm = AIMessage(content=(
            "## ✅ Plan Approved!\n\n"
            "Your personalised financial plan has been finalised. "
            "The report has been saved to `financial_plan.md`.\n\n"
            "**Next steps:** Share this plan with a SEBI-registered financial advisor "
            "for professional validation before making investment decisions.\n\n"
            "*FinSage — AI Money Mentor | ET AI Hackathon 2026*"
        ))
        return {
            "human_approved": True,
            "messages": [confirm],
        }

    # User wants refinement
    refine_msg = AIMessage(content=(
        f"## 🔄 Refining Your Plan\n\n"
        f"Noted: _{feedback}_\n\n"
        f"Re-running analysis with your feedback in mind..."
    ))
    return {
        "human_approved": False,
        "human_feedback": feedback,
        # Reset completed tasks so agents re-run
        "tasks_completed": [],
        "tasks_requested": ["fire", "tax", "insurance"],
        "messages": [refine_msg],
    }


# ─── Node 9: Life Event Advisor ───────────────────────────────────────────────

def life_event_advisor_node(state: MoneyMentorState) -> dict:
    """
    Life Event Financial Advisor Agent

    Handles bonus, marriage, baby, inheritance, job_change events.
    Generates a tailored action plan with specific rupee amounts.
    """
    profile = state.get("user_profile", {})
    event = state.get("life_event_data", {}) or {}

    event_type = event.get("event_type", "bonus")
    amount = float(event.get("amount_involved", 0))
    description = event.get("description", "")

    age = profile.get("age", 30)
    monthly_income = float(profile.get("monthly_income", 50000))
    risk_profile = profile.get("risk_profile", "moderate")
    existing_ef = float(profile.get("emergency_fund", 0))
    monthly_expenses = float(profile.get("monthly_expenses", 30000))
    ef_target = monthly_expenses * 6

    recommendations: list[str] = []
    action_items: list[str] = []
    split: dict = {}

    if event_type == "bonus":
        ef_gap = max(0.0, ef_target - existing_ef)
        ef_allocation = min(amount * 0.30, ef_gap)
        invest_amount = amount - ef_allocation
        equity_pct = 0.60 if risk_profile == "aggressive" else 0.40 if risk_profile == "moderate" else 0.20
        split = {
            "emergency_fund_topup": round(ef_allocation),
            "equity_mf_lumpsum": round(invest_amount * equity_pct),
            "debt_ppf_fd": round(invest_amount * (1 - equity_pct) * 0.70),
            "liquid_goal_fund": round(invest_amount * (1 - equity_pct) * 0.30),
        }
        recommendations.append(f"Deposit ₹{split['emergency_fund_topup']:,} in emergency fund (liquid FD/savings)")
        recommendations.append(f"Invest ₹{split['equity_mf_lumpsum']:,} via MF lumpsum in index/flexi cap fund (STF if market high)")
        recommendations.append(f"Park ₹{split['debt_ppf_fd']:,} in PPF or short-duration debt fund")
        recommendations.append(f"Keep ₹{split['liquid_goal_fund']:,} for near-term goals")
        action_items = ["Transfer EF amount to separate savings account today",
                        "Use STP (Systematic Transfer Plan) for equity investment over 6 months",
                        "Check if 80C limit exhausted — book ELSS from bonus"]

    elif event_type in ("marriage", "wedding"):
        split = {
            "joint_emergency_fund": round(amount * 0.20),
            "home_down_payment_corpus": round(amount * 0.30),
            "joint_equity_sip_start": round(monthly_income * 0.25),
            "gold_sovereign_bond": round(amount * 0.15),
            "honeymoon_vacation": round(amount * 0.10),
            "contingency": round(amount * 0.25),
        }
        recommendations.append("Open joint Demat and MF account with spouse")
        recommendations.append("Review and update all insurance nominees immediately")
        recommendations.append(f"Start joint SIP of ₹{split['joint_equity_sip_start']:,}/month for home purchase goal")
        recommendations.append("Buy Sovereign Gold Bonds for bridal gold at market rate")
        action_items = ["Update PAN/Aadhaar address", "Add spouse to health insurance as family floater",
                        "Make new Will reflecting changed family status",
                        "Optimise HRA — higher income earner should claim rent"]

    elif event_type == "baby":
        corpus_target = 5000000 if age < 35 else 8000000
        sip_needed = calculate_sip_required.invoke({
            "corpus_needed": corpus_target, "years": 18,
            "expected_return_rate": 12.0, "existing_corpus": 0,
        })
        split = {
            "child_education_sip": sip_needed["monthly_sip"],
            "health_cover_upgrade": 200000,
            "life_cover_increase": max(0, (monthly_income * 12 * 12) - float(profile.get("existing_life_cover", 0))),
        }
        recommendations.append(f"Start SIP of ₹{sip_needed['monthly_sip']:,}/month in ELSS/Flexi Cap for child's education")
        recommendations.append(f"Add child to health insurance — upgrade family floater to ₹{split['health_cover_upgrade']:,}")
        recommendations.append(f"Review term cover: should be 12x annual income = ₹{monthly_income*12*12:,.0f}")
        action_items = ["Open minor folio in PPFAS Flexi Cap Fund",
                        "Start SSY (Sukanya Samriddhi Yojana) if girl child — 8.2% p.a.",
                        "Update nominees on all policies and MF folios",
                        "Write a Will immediately — critical with a child"]

    elif event_type == "inheritance":
        equity = round(amount * 0.40)
        debt = round(amount * 0.30)
        gold = round(amount * 0.10)
        re = round(amount * 0.15)
        liquid = round(amount * 0.05)
        split = {"equity_mfs": equity, "debt_ppf_fd": debt, "gold_sgb": gold,
                 "real_estate_or_reit": re, "liquid_fund": liquid}
        recommendations.append(f"Park full ₹{amount:,.0f} in liquid fund for 3 months — do not rush decisions")
        recommendations.append(f"Invest ₹{equity:,} in diversified equity MFs via STP over 12 months")
        recommendations.append(f"Buy ₹{gold:,} worth of Sovereign Gold Bonds (8.2%+gold returns)")
        recommendations.append("Consult CA for tax on inheritance: immovable property transfer implications")
        action_items = ["File ITR with inheritance details", "Get property valuation if land/property inherited",
                        "Update Will with new assets", "No income tax on inherited money — only on income it generates"]

    elif event_type == "job_change":
        new_income = amount if amount > monthly_income * 12 else monthly_income * 1.5 * 12
        hike = new_income - monthly_income * 12
        sip_increase = round(hike * 0.50 / 12)
        split = {
            "sip_hike_monthly": sip_increase,
            "pf_transfer_amount": round(float(profile.get("pf_balance", 0))),
            "esop_vesting_value": round(amount * 0.30) if amount > 0 else 0,
        }
        recommendations.append(f"Increase monthly SIP by ₹{sip_increase:,} (50% of salary hike goes to investments)")
        recommendations.append("Transfer EPF to new employer — do NOT withdraw (tax implications + missed compounding)")
        recommendations.append("Review new employer's group health cover — supplement if below ₹5L")
        recommendations.append("Update 80C/NPS declarations with new payroll team")
        action_items = ["Initiate EPF transfer on EPFO portal within 30 days",
                        "Get Form 16 from old employer", "Inform bank/MF/insurance of address change if relocated",
                        "Re-negotiate joining bonus for tax impact — ask for it to be structured as reimbursements"]

    else:
        recommendations = ["Consult a SEBI-registered financial advisor for tailored advice on this event"]
        action_items = ["Document all financial decisions made around this event"]
        split = {}

    # LLM narrative
    narrative = _llm_narrative(
        prompt=(
            f"In 3 sentences, provide specific financial advice for a {age}-year-old experiencing "
            f"'{event_type}' with ₹{amount:,.0f} involved. Income ₹{monthly_income:,.0f}/month. "
            f"Be actionable and specific to Indian financial instruments."
        ),
        fallback=f"This is a significant life event. Act decisively with a clear allocation plan.",
    )

    result = {
        "event_type": event_type,
        "amount_involved": amount,
        "split_recommendation": split,
        "recommendations": recommendations,
        "action_items": action_items,
        "narrative": narrative,
    }

    rec_str = "\n".join(f"- {r}" for r in recommendations)
    action_str = "\n".join(f"{i+1}. {a}" for i, a in enumerate(action_items))

    msg = AIMessage(content=(
        f"## 🎯 Life Event Advisor — {event_type.replace('_',' ').title()}\n\n"
        f"**Event:** {description or event_type}\n"
        f"**Amount involved:** {_inr(amount)}\n\n"
        f"**Recommended Allocation:**\n"
        + "\n".join(f"- {k.replace('_',' ').title()}: {_inr(v)}" for k, v in split.items() if v > 0) +
        f"\n\n**Strategy:**\n{rec_str}\n\n"
        f"**Action Items:**\n{action_str}\n\n"
        f"> {narrative}"
    ))

    tasks_completed = list(state.get("tasks_completed", [])) + ["life_event"]
    return {
        "life_event_result": result,
        "tasks_completed": tasks_completed,
        "current_agent": "life_event_advisor",
        "messages": [msg],
    }


# ─── Node 10: Couple Planner ──────────────────────────────────────────────────

def couple_planner_node(state: MoneyMentorState) -> dict:
    """
    Couple's Money Planner Agent

    Optimises across two incomes: HRA, NPS, SIP splits, joint goals.
    Demonstrates multi-input agent with cross-user analysis.
    """
    p1 = state.get("user_profile", {})
    p2 = state.get("couple_data", {}) or {}

    name1 = p1.get("name", "Partner 1")
    name2 = p2.get("name", "Partner 2")
    income1 = float(p1.get("monthly_income", 0))
    income2 = float(p2.get("monthly_income", 0))
    expenses1 = float(p1.get("monthly_expenses", 0))
    expenses2 = float(p2.get("monthly_expenses", 0))
    age1 = p1.get("age", 30)
    age2 = p2.get("age", 30)
    combined_income = income1 + income2
    combined_expenses = expenses1 + expenses2
    combined_savings = combined_income - combined_expenses

    # HRA Optimisation — higher earner in rented city claims HRA
    hra1 = float(p1.get("existing_savings", 0)) * 0  # simplified
    hra_recommendation = (
        f"{name1} should claim HRA (higher income)"
        if income1 > income2
        else f"{name2} should claim HRA (higher income)"
    )

    # NPS: Both should max NPS for extra ₹50k deduction each
    nps_saving_combined = 50000 * 2  # both max out 80CCD(1B)
    tax1 = calculate_tax_liability.invoke({
        "annual_income": income1 * 12, "deductions": {"NPS_80CCD": 50000}, "regime": "old"
    })
    tax2 = calculate_tax_liability.invoke({
        "annual_income": income2 * 12, "deductions": {"NPS_80CCD": 50000}, "regime": "old"
    })

    # SIP Split — aggressive for younger, conservative for older
    risk1 = p1.get("risk_profile", "moderate")
    risk2 = p2.get("risk_profile", "moderate")
    total_investable = combined_savings * 0.60
    sip1 = round(total_investable * (income1 / max(combined_income, 1)))
    sip2 = round(total_investable * (income2 / max(combined_income, 1)))

    # Joint goals
    joint_retirement_corpus = calculate_retirement_corpus.invoke({
        "current_monthly_expenses": combined_expenses,
        "current_age": min(age1, age2),
        "retirement_age": max(p1.get("retirement_age", 60), p2.get("retirement_age", 60)),
        "life_expectancy": 85,
        "inflation_rate": 6.0,
        "post_retirement_return": 7.0,
    })

    combined_net_worth = (
        float(p1.get("mf_portfolio_value", 0)) + float(p1.get("stock_portfolio", 0)) +
        float(p1.get("real_estate_value", 0)) + float(p1.get("pf_balance", 0)) +
        float(p2.get("mf_portfolio_value", 0)) + float(p2.get("stock_portfolio", 0)) +
        float(p2.get("real_estate_value", 0)) + float(p2.get("pf_balance", 0))
    )

    couple_plan = {
        "combined_income": combined_income,
        "combined_expenses": combined_expenses,
        "combined_savings": combined_savings,
        "combined_net_worth": combined_net_worth,
        "hra_recommendation": hra_recommendation,
        "nps_recommendation": {"each_max": 50000, "combined_tax_saving": nps_saving_combined},
        "sip_split": {name1: sip1, name2: sip2, "total_monthly": sip1 + sip2},
        "joint_retirement_corpus": joint_retirement_corpus["corpus_required"],
        "joint_retirement_years": joint_retirement_corpus["years_to_retirement"],
    }

    narrative = _llm_narrative(
        prompt=(
            f"In 3 sentences, give financial planning advice for a couple: "
            f"{name1} (age {age1}, ₹{income1:,.0f}/month, {risk1}) and "
            f"{name2} (age {age2}, ₹{income2:,.0f}/month, {risk2}). "
            f"Combined income ₹{combined_income:,.0f}. Focus on Indian instruments."
        ),
        fallback=(
            f"As a couple with combined income of {_inr(combined_income)}/month, "
            f"max NPS for both, optimize HRA, and split SIPs proportional to income."
        ),
    )

    msg = AIMessage(content=(
        f"## 💑 Couple's Money Planner\n\n"
        f"| Metric | {name1} | {name2} | Combined |\n|---|---|---|---|\n"
        f"| Monthly Income | {_inr(income1)} | {_inr(income2)} | **{_inr(combined_income)}** |\n"
        f"| Monthly Expenses | {_inr(expenses1)} | {_inr(expenses2)} | {_inr(combined_expenses)} |\n"
        f"| Monthly Savings | {_inr(income1-expenses1)} | {_inr(income2-expenses2)} | **{_inr(combined_savings)}** |\n"
        f"| SIP Allocation | {_inr(sip1)}/mo | {_inr(sip2)}/mo | {_inr(sip1+sip2)}/mo |\n\n"
        f"**🏠 HRA Optimisation:** {hra_recommendation}\n\n"
        f"**📊 NPS Strategy:** Both max NPS 80CCD(1B) — combined deduction ₹1L/year\n"
        f"- {name1}: NPS saves ~{_inr(round(tax1['total_tax'] * 0.15))}/year\n"
        f"- {name2}: NPS saves ~{_inr(round(tax2['total_tax'] * 0.15))}/year\n\n"
        f"**🎯 Joint Retirement Goal:**\n"
        f"- Corpus needed: {_inr(joint_retirement_corpus['corpus_required'])}\n"
        f"- Years to goal: {joint_retirement_corpus['years_to_retirement']} years\n"
        f"- Combined monthly SIP needed: {_inr(sip1+sip2)}\n\n"
        f"**💰 Combined Net Worth:** {_inr(combined_net_worth)}\n\n"
        f"> {narrative}"
    ))

    tasks_completed = list(state.get("tasks_completed", [])) + ["couple"]
    return {
        "couple_plan_result": couple_plan,
        "tasks_completed": tasks_completed,
        "current_agent": "couple_planner",
        "messages": [msg],
    }


# ─── Node 11: MF Portfolio X-Ray ──────────────────────────────────────────────

def mf_xray_node(state: MoneyMentorState) -> dict:
    """
    Mutual Fund Portfolio X-Ray Agent

    Analyses MF holdings for:
    - Portfolio reconstruction (true XIRR, overlap, expense drag)
    - Benchmark comparison
    - Rebalancing recommendations
    """
    holdings = state.get("mf_holdings") or []
    profile = state.get("user_profile", {})

    if not holdings:
        msg = AIMessage(content="⚠️ No MF holdings found. Please upload your CAMS/KFintech statement.")
        return {"mf_xray_result": {}, "messages": [msg]}

    total_invested = sum(float(h.get("invested_amount", 0) or 0) for h in holdings)
    total_current = sum(float(h.get("current_value", 0) or 0) for h in holdings)
    total_gain = total_current - total_invested
    total_gain_pct = (total_gain / total_invested * 100) if total_invested > 0 else 0

    # Weighted XIRR
    weighted_xirr = (
        sum(float(h.get("xirr", 0) or 0) * float(h.get("current_value", 0) or 0) for h in holdings)
        / max(total_current, 1)
    )

    # Weighted expense ratio
    weighted_er = (
        sum(float(h.get("expense_ratio", 0) or 0) * float(h.get("current_value", 0) or 0) for h in holdings)
        / max(total_current, 1)
    )

    # Category allocation
    category_values: dict[str, float] = {}
    for h in holdings:
        cat = h.get("category", "Other")
        category_values[cat] = category_values.get(cat, 0) + float(h.get("current_value", 0) or 0)
    category_pct = {k: round(v / max(total_current, 1) * 100, 1) for k, v in category_values.items()}

    # Overlap detection (funds with same category = potential overlap)
    from collections import Counter
    cat_counts = Counter(h.get("category") for h in holdings)
    overlapping = [cat for cat, cnt in cat_counts.items() if cnt > 2]

    # Expense drag (cost of high expense ratio vs direct index)
    index_er = 0.0019  # UTI Nifty 50 Direct expense ratio
    excess_cost_pa = (weighted_er - index_er) * total_current

    # Recommendations
    recommendations: list[str] = []
    age = profile.get("age", 30)
    risk = profile.get("risk_profile", "moderate")

    target_alloc = suggest_asset_allocation.invoke({"age": age, "risk_profile": risk})
    equity_target = target_alloc["equity_pct"]
    current_equity_pct = sum(
        category_pct.get(c, 0) for c in ["Large Cap", "Mid Cap", "Small Cap", "Flexi Cap", "Index", "ELSS", "Sectoral", "International"]
    )

    if overlapping:
        recommendations.append(f"Overlap detected in {', '.join(overlapping)} — consolidate to fewer funds")
    if weighted_er > 0.0100:
        recommendations.append(f"Expense ratio {weighted_er*100:.2f}% is high — shift some allocation to index funds (0.10-0.19%)")
    if abs(current_equity_pct - equity_target) > 10:
        action = "Reduce" if current_equity_pct > equity_target else "Increase"
        recommendations.append(f"{action} equity from {current_equity_pct:.0f}% to target {equity_target:.0f}%")
    if not any(h.get("category") == "Index" for h in holdings):
        recommendations.append("Add UTI Nifty 50 / HDFC Index Fund for low-cost core allocation (20-30%)")
    if not any(h.get("category") == "International" for h in holdings) and risk == "aggressive":
        recommendations.append("Add international fund (Nasdaq 100 / S&P 500 FoF) for global diversification (5-10%)")
    if not recommendations:
        recommendations.append("Portfolio is well-diversified — maintain current allocation")

    xray_result = {
        "total_invested": total_invested,
        "total_current": total_current,
        "total_gain": total_gain,
        "total_gain_pct": round(total_gain_pct, 2),
        "weighted_xirr": round(weighted_xirr, 2),
        "weighted_expense_ratio_pct": round(weighted_er * 100, 4),
        "annual_expense_drag": round(excess_cost_pa),
        "category_allocation": category_pct,
        "overlapping_categories": overlapping,
        "recommendations": recommendations,
        "fund_count": len(holdings),
        "target_equity_pct": equity_target,
        "current_equity_pct": round(current_equity_pct, 1),
    }

    narrative = _llm_narrative(
        prompt=(
            f"In 3 sentences, analyse this MF portfolio: invested ₹{total_invested:,.0f}, "
            f"current ₹{total_current:,.0f}, XIRR {weighted_xirr:.1f}%, "
            f"expense ratio {weighted_er*100:.2f}%, {len(holdings)} funds. "
            f"Give specific rebalancing advice for a {age}-year-old {risk} investor."
        ),
        fallback=f"Your MF portfolio has grown by {total_gain_pct:.1f}%. Review and rebalance annually.",
    )

    fund_rows = "\n".join(
        f"| {h.get('fund_name','')[:40]} | {h.get('category','')} | "
        f"{_inr(float(h.get('invested_amount',0)))} | {_inr(float(h.get('current_value',0)))} | "
        f"{h.get('xirr',0):.1f}% | {float(h.get('expense_ratio',0))*100:.2f}% |"
        for h in holdings[:10]
    )

    cat_str = "\n".join(f"- {k}: {v}%" for k, v in sorted(category_pct.items(), key=lambda x: -x[1]))
    rec_str = "\n".join(f"- {r}" for r in recommendations)

    msg = AIMessage(content=(
        f"## 🔬 MF Portfolio X-Ray\n\n"
        f"| Metric | Value |\n|---|---|\n"
        f"| Total Invested | **{_inr(total_invested)}** |\n"
        f"| Current Value | **{_inr(total_current)}** |\n"
        f"| Total Gain | {_inr(total_gain)} ({total_gain_pct:.1f}%) |\n"
        f"| Weighted XIRR | **{weighted_xirr:.2f}%** |\n"
        f"| Avg Expense Ratio | {weighted_er*100:.3f}% |\n"
        f"| Annual Expense Drag | {_inr(excess_cost_pa)} extra vs Index |\n"
        f"| No. of Funds | {len(holdings)} |\n\n"
        f"**Category Allocation:**\n{cat_str}\n\n"
        f"**Fund Details:**\n"
        f"| Fund Name | Category | Invested | Current | XIRR | ER |\n|---|---|---|---|---|---|\n"
        f"{fund_rows}\n\n"
        f"**Rebalancing Recommendations:**\n{rec_str}\n\n"
        f"> {narrative}"
    ))

    tasks_completed = list(state.get("tasks_completed", [])) + ["mf_xray"]
    return {
        "mf_xray_result": xray_result,
        "tasks_completed": tasks_completed,
        "current_agent": "mf_xray",
        "messages": [msg],
    }
