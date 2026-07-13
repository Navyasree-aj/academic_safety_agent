# src/nodes/basic_nodes.py
from src.state import AgentState

def perception_evaluator_node(state: AgentState) -> dict:
    """
    Simulates parsing student metrics and determining a baseline risk layer.
    """
    print("\n--- Executing Perception Evaluator Node ---")
    
    attendance = state.get("attendance_percentage", 100.0)
    marks = state.get("recent_marks", [])
    
    # Simple rules for today's foundation build
    avg_mark = sum(marks) / len(marks) if marks else 100.0
    
    current_logs = state.get("logs", [])
    current_logs.append(f"Evaluated data: Attendance={attendance}%, AvgMark={avg_mark}%")
    
    # Preliminary classification logic
    if attendance < 75.0 or avg_mark < 50.0:
        risk = "Critical"
    elif attendance < 85.0 or avg_mark < 70.0:
        risk = "Medium"
    else:
        risk = "Low"
        
    return {
        "calculated_risk_level": risk,
        "logs": current_logs
    }

def action_execution_node(state: AgentState) -> dict:
    """
    Simulates executing an intervention action based on the evaluated risk level.
    """
    print("\n--- Executing Action Execution Node ---")
    risk = state.get("calculated_risk_level", "Low")
    current_logs = state.get("logs", [])
    
    action_taken = f"Executed default action for {risk} risk mitigation."
    current_logs.append(action_taken)
    
    print(f"[ACTION TAKEN] {action_taken}")
    
    return {
        "logs": current_logs,
        "next_step": "completed"
    }