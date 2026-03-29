"""
LangGraph Workflow for FinSage — AI Money Mentor

Demonstrates the following LangGraph concepts:
  1.  StateGraph with TypedDict state
  2.  add_node — 11 distinct agent nodes
  3.  add_edge — deterministic sequential flow
  4.  add_conditional_edges — dynamic routing (3 different routers)
  5.  ToolNode — tool execution layer (bound to financial_tools)
  6.  MemorySaver — persistent checkpointing across turns
  7.  interrupt_before — human-in-the-loop pause
  8.  Supervisor multi-agent pattern
  9.  Cyclic graph — refinement loop back to supervisor
  10. Life Event, Couple Planner, MF X-Ray specialist agents

Graph topology:
  START
    │
    ▼
  [profile_collector] ──(profile incomplete)──►[profile_collector] (loop)
    │ (profile complete)
    ▼
  [health_scorer]
    │
    ▼
  [supervisor] ◄──────────────────────────────────────────────────────────────────┐
    │                                                                              │
    ├──► [fire_planner]       ────────────────────────────────────────────────► │ │
    ├──► [tax_optimizer]      ────────────────────────────────────────────────► │ │
    ├──► [insurance_auditor]  ────────────────────────────────────────────────► │ │
    ├──► [life_event_advisor] ────────────────────────────────────────────────► │ │
    ├──► [couple_planner]     ────────────────────────────────────────────────► │ │
    ├──► [mf_xray]            ────────────────────────────────────────────────► │ │
    │                                                                            │ │
    └──► [report_generator]                                                      │ │
              │                                                                  │ │
              ▼                                                                  │ │
         [human_review] ──(not approved, iter < 4)──────────────────────────────┘ │
              │ (approved OR max iterations)                                        │
              ▼                                                                     │
             END                                                                    │
"""
from __future__ import annotations

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode

from src.nodes import (
    couple_planner_node,
    fire_planner_node,
    health_scorer_node,
    human_review_node,
    insurance_auditor_node,
    life_event_advisor_node,
    mf_xray_node,
    profile_collector_node,
    report_generator_node,
    supervisor_node,
    tax_optimizer_node,
)
from src.state import MoneyMentorState
from src.tools import financial_tools


# ─── Router Functions ─────────────────────────────────────────────────────────

def route_after_profile(state: MoneyMentorState) -> str:
    """
    Conditional edge: decide whether to loop for more profile data or proceed.
    Returns "health_scorer" — profile is complete, move forward
    Returns "profile_collector" — still gathering data, loop back
    """
    return "health_scorer" if state.get("profile_complete") else "profile_collector"


def supervisor_router(state: MoneyMentorState) -> str:
    """
    Conditional edge: supervisor decides which agent runs next.
    Priority: fire → tax → insurance → life_event → couple → mf_xray → report
    """
    requested = set(state.get("tasks_requested", []))
    completed = set(state.get("tasks_completed", []))
    remaining = requested - completed

    priority = ["fire", "tax", "insurance", "life_event", "couple", "mf_xray"]
    for task in priority:
        if task in remaining:
            return task

    return "report_generator"


def route_after_review(state: MoneyMentorState) -> str:
    """
    Conditional edge: after human review, finish or refine.
    Returns END — approved or max iterations reached
    Returns "supervisor" — user wants changes (refinement loop)
    """
    if state.get("human_approved"):
        return END
    if state.get("iteration", 0) >= 4:
        return END
    return "supervisor"


# ─── Graph Builder ────────────────────────────────────────────────────────────

def build_graph(use_hitl: bool = True):
    """
    Build and compile the FinSage multi-agent LangGraph.

    Args:
        use_hitl: If True, graph pauses before human_review for user input.

    Returns:
        Compiled LangGraph with MemorySaver checkpointing.
    """
    builder = StateGraph(MoneyMentorState)

    # ── 1. Register all 11 agent nodes ────────────────────────────────────
    builder.add_node("profile_collector",  profile_collector_node)
    builder.add_node("health_scorer",      health_scorer_node)
    builder.add_node("supervisor",         supervisor_node)
    builder.add_node("fire_planner",       fire_planner_node)
    builder.add_node("tax_optimizer",      tax_optimizer_node)
    builder.add_node("insurance_auditor",  insurance_auditor_node)
    builder.add_node("life_event_advisor", life_event_advisor_node)
    builder.add_node("couple_planner",     couple_planner_node)
    builder.add_node("mf_xray",            mf_xray_node)
    builder.add_node("report_generator",   report_generator_node)
    builder.add_node("human_review",       human_review_node)

    # ── 2. Tool node (LLM-driven tool calling future extension) ───────────
    tool_node = ToolNode(financial_tools)
    builder.add_node("tools", tool_node)

    # ── 3. Entry point ────────────────────────────────────────────────────
    builder.add_edge(START, "profile_collector")

    # ── 4. Conditional: profile check loop ────────────────────────────────
    builder.add_conditional_edges(
        "profile_collector",
        route_after_profile,
        {
            "health_scorer":     "health_scorer",
            "profile_collector": "profile_collector",
        },
    )

    # ── 5. Linear: health scorer → supervisor ─────────────────────────────
    builder.add_edge("health_scorer", "supervisor")

    # ── 6. Conditional: supervisor dispatches to 6 specialist agents ──────
    builder.add_conditional_edges(
        "supervisor",
        supervisor_router,
        {
            "fire":             "fire_planner",
            "tax":              "tax_optimizer",
            "insurance":        "insurance_auditor",
            "life_event":       "life_event_advisor",
            "couple":           "couple_planner",
            "mf_xray":          "mf_xray",
            "report_generator": "report_generator",
        },
    )

    # ── 7. All specialist agents return to supervisor ──────────────────────
    for node in ("fire_planner", "tax_optimizer", "insurance_auditor",
                 "life_event_advisor", "couple_planner", "mf_xray"):
        builder.add_edge(node, "supervisor")

    # ── 8. Report → human review ──────────────────────────────────────────
    builder.add_edge("report_generator", "human_review")

    # ── 9. Conditional: human review → refine cycle or END ────────────────
    builder.add_conditional_edges(
        "human_review",
        route_after_review,
        {
            "supervisor": "supervisor",
            END: END,
        },
    )

    # ── 10. Compile with checkpointing & HITL ─────────────────────────────
    memory = MemorySaver()
    interrupt_nodes = ["human_review"] if use_hitl else []

    return builder.compile(
        checkpointer=memory,
        interrupt_before=interrupt_nodes,
    )


# ─── Convenience: default initial state ──────────────────────────────────────

def make_initial_state(profile: dict) -> dict:
    """Create a clean initial MoneyMentorState from a user profile dict."""
    return {
        "messages": [],
        "user_profile": profile,
        "profile_complete": False,   # profile_collector will validate & set True
        "health_score_result": None,
        "fire_plan_result": None,
        "tax_analysis_result": None,
        "insurance_analysis_result": None,
        "tasks_requested": [],
        "tasks_completed": [],
        "current_agent": "profile_collector",
        "human_approved": False,
        "human_feedback": None,
        "final_report": None,
        "iteration": 0,
        "error_message": None,
    }
