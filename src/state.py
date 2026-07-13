# src/state.py
from typing import TypedDict, List, Optional

class AgentState(TypedDict):
    """
    Represents the internal shared memory state of our 
    Autonomous Student Risk & Escalation Agent.
    """
    student_id: str
    attendance_percentage: float
    recent_marks: List[float]
    calculated_risk_level: Optional[str]  # "Low", "Medium", "Critical"
    urgency_score: Optional[float]        # Numeric value tracking urgency
    next_step: Optional[str]              # Used for routing decisions
    logs: List[str]                       # Audit trail of what the agent has done