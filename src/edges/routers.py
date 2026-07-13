# src/edges/routers.py
from src.state import AgentState

def risk_routing_edge(state: AgentState) -> str:
    """
    Inspects the state and returns the next destination node string name.
    """
    risk = state.get("calculated_risk_level", "Low")
    if risk in ["Medium", "Critical"]:
        return "trigger_escalation"
    return "end_workflow"