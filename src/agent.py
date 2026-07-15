# src/agent.py
from langgraph.graph import StateGraph, START, END
from src.state import AgentState
from src.nodes.basic_nodes import perception_evaluator_node, urgency_scalar_node, action_execution_node
from src.edges.routers import risk_routing_edge

def compile_agent():
    workflow = StateGraph(AgentState)
    
    # 1. Register all three operational nodes
    workflow.add_node("perception_evaluator", perception_evaluator_node)
    workflow.add_node("urgency_scalar", urgency_scalar_node)
    workflow.add_node("action_executor", action_execution_node)
    
    # 2. Establish linear flow from perception to mathematical evaluation
    workflow.add_edge(START, "perception_evaluator")
    workflow.add_edge("perception_evaluator", "urgency_scalar") # New connection!
    
    # 3. Bind conditional routing evaluating the complete state from the scalar output
    workflow.add_conditional_edges(
        "urgency_scalar", # The router now fires AFTER math execution completes
        risk_routing_edge,
        {
            "trigger_escalation": "action_executor",
            "end_workflow": END
        }
    )
    
    workflow.add_edge("action_executor", END)
    
    return workflow.compile()

agent_executor = compile_agent()