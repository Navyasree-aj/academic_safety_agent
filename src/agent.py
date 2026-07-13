# src/agent.py
from langgraph.graph import StateGraph, END
from src.state import AgentState
from src.nodes.basic_nodes import perception_evaluator_node, action_execution_node
from src.edges.routers import risk_routing_edge

def compile_agent():
    # Initialize the graph with our formal State schema
    workflow = StateGraph(AgentState)
    
    # Register our processing nodes
    workflow.add_node("perception_evaluator", perception_evaluator_node)
    workflow.add_node("action_executor", action_execution_node)
    
    # Establish Entry Point
    workflow.set_entry_point("perception_evaluator")
    
    # Register Conditional Edge routing from the perception evaluator
    workflow.add_conditional_edges(
        "perception_evaluator",
        risk_routing_edge,
        {
            "trigger_escalation": "action_executor",
            "end_workflow": END
        }
    )
    
    # Connect the final action node directly to structural completion
    workflow.add_edge("action_executor", END)
    
    # Compile the graph into an executable runnable instance
    return workflow.compile()

# Instantiated runnable
agent_executor = compile_agent()