# src/state.py
from typing import Any, TypedDict, List, Optional, Dict

class AgentState(TypedDict):
    """
    The expanded memory state for our reasoning loop.
    """
    student_id: str
    student_name: Optional[str]
    student_email: Optional[str]
    
    # Raw ingested data components from our PostgreSQL database
    perception_data: Optional[dict]
    
    # Evaluated AI metrics
    calculated_risk_level: Optional[str]   # "Low", "Medium", or "Critical"
    reasoning_summary: Optional[str]       # Explanatory text from LLaMA
    urgency_score: Optional[float]
    
    logs: List[str]

    # --- New Core Features Fields ---
    trigger_batch_insight: Optional[bool]
    batch_failure_rate: Optional[float]
    missed_topic_data: Optional[Dict[str, Any]]