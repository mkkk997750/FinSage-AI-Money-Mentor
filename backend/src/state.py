"""
LangGraph State Definition for FinSage - AI Money Mentor

Demonstrates:
  - TypedDict-based state schema
  - Annotated[list, add_messages] for automatic message accumulation
  - Optional fields for incremental agent updates
"""
from __future__ import annotations

from typing import Annotated, List, Optional

from langgraph.graph.message import add_messages
from typing_extensions import TypedDict


class MoneyMentorState(TypedDict, total=False):
    """
    Shared state that flows through every node in the LangGraph workflow.

    Fields marked Optional are populated incrementally:
      - profile_collector  → user_profile, profile_complete
      - health_scorer      → health_score_result
      - fire_planner       → fire_plan_result
      - tax_optimizer      → tax_analysis_result
      - insurance_auditor  → insurance_analysis_result
      - report_generator   → final_report
      - human_review       → human_approved, human_feedback
    """

    # ── Conversation history (accumulated automatically by LangGraph) ────────
    messages: Annotated[list, add_messages]

    # ── User financial profile ───────────────────────────────────────────────
    user_profile: Optional[dict]
    profile_complete: bool

    # ── Analysis results (set by individual agent nodes) ────────────────────
    health_score_result: Optional[dict]
    fire_plan_result: Optional[dict]
    tax_analysis_result: Optional[dict]
    insurance_analysis_result: Optional[dict]
    life_event_result: Optional[dict]
    couple_plan_result: Optional[dict]
    mf_xray_result: Optional[dict]

    # ── Extra input data for specialist agents ────────────────────────────────
    life_event_data: Optional[dict]   # event_type, amount, description
    couple_data: Optional[dict]       # partner2 profile
    mf_holdings: Optional[list]       # list of MF holding dicts from DB

    # ── Workflow control (supervisor orchestration) ──────────────────────────
    tasks_requested: List[str]   # e.g. ["fire", "tax", "insurance", "life_event", "couple", "mf_xray"]
    tasks_completed: List[str]   # grows as each agent finishes
    current_agent: str           # for logging / debugging

    # ── Human-in-the-loop ────────────────────────────────────────────────────
    human_approved: bool
    human_feedback: Optional[str]
    iteration: int               # tracks refinement cycles

    # ── Final output ─────────────────────────────────────────────────────────
    final_report: Optional[str]
    error_message: Optional[str]
