"""
Pydantic models for FinSage API request/response types
"""
from __future__ import annotations

from typing import Any, Optional
from pydantic import BaseModel, Field


class AgentRequest(BaseModel):
    user_id: int = Field(..., description="User ID from the users table")
    message: str = Field(default="", description="User message or question")
    session_id: Optional[str] = Field(default=None)
    agent_type: Optional[str] = Field(default="full")
    tasks_requested: Optional[list[str]] = Field(default=None)


class LifeEventRequest(BaseModel):
    user_id: int
    event_type: str = Field(..., description="bonus|marriage|baby|inheritance|job_change|home_purchase")
    amount_involved: float = Field(default=0.0)
    description: str = Field(default="")
    session_id: Optional[str] = None


class CouplePlanRequest(BaseModel):
    user1_id: int
    user2_id: int
    session_id: Optional[str] = None


class MFXrayRequest(BaseModel):
    user_id: int
    session_id: Optional[str] = None


class ChatRequest(BaseModel):
    user_id: int
    message: str
    session_id: str
    agent_type: str = Field(default="full")


class AgentResponse(BaseModel):
    session_id: str
    agent_type: str
    messages: list[dict]
    result: Optional[dict] = None
    status: str = "success"
    error: Optional[str] = None


class UserSummary(BaseModel):
    user_id: int
    name: str
    age: int
    city: str
    occupation: str
    monthly_income: Optional[float] = None
    risk_profile: Optional[str] = None
    overall_health_score: Optional[float] = None
    grade: Optional[str] = None
