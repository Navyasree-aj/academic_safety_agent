# src/edges/routers.py
from src.state import AgentState

def risk_routing_edge(state: AgentState) -> str:
    """
    Evaluates the risk level produced by the LLM and routes the graph state.
    """
    # Read the AI's calculation from the shared state
    risk = state.get("calculated_risk_level", "Low")
    
    if risk in ["Medium", "Critical"]:
        return "trigger_escalation"
    
    return "end_workflow"