# src/agent.py
from langgraph.graph import StateGraph, START, END
from src.state import AgentState
from src.nodes.basic_nodes import perception_evaluator_node, urgency_scalar_node, action_execution_node

def compile_agent():
    workflow = StateGraph(AgentState)
    
    # 1. Register all three operational nodes
    workflow.add_node("perception_evaluator", perception_evaluator_node)
    workflow.add_node("urgency_scalar", urgency_scalar_node)
    workflow.add_node("action_executor", action_execution_node)
    
    # 2. Establish complete linear flow across all evaluation and tracking nodes
    workflow.add_edge(START, "perception_evaluator")
    workflow.add_edge("perception_evaluator", "urgency_scalar")
    workflow.add_edge("urgency_scalar", "action_executor")  # Direct flow to execution node
    workflow.add_edge("action_executor", END)
    
    return workflow.compile()

agent_executor = compile_agent()