from langgraph.graph import StateGraph, END
from src.state import AgentState
from src.nodes.retrieval import retrieval_node
from src.nodes.generation import generation_node
from src.nodes.validation import validation_node
from src.nodes.execution import execution_node
from src.nodes.explanation import explanation_node

def should_retry(state: AgentState):
    """Decides whether to retry SQL generation or explain result."""
    if state.get("error"):
        if state.get("retry_count", 0) < 3:
            return "retry"
        else:
            return "fail"
    return "execute"

def validate_transition(state: AgentState):
    """Checks if validation passed."""
    if state.get("error"):
        return "generate" # Try re-generating if validation fails
    return "execute"

def define_graph():
    """Defines the workflow graph."""
    workflow = StateGraph(AgentState)

    # Add Nodes
    workflow.add_node("retrieve", retrieval_node)
    workflow.add_node("generate", generation_node)
    workflow.add_node("validate", validation_node)
    workflow.add_node("execute", execution_node)
    workflow.add_node("explain", explanation_node)

    # Set Entry Point
    workflow.set_entry_point("retrieve")

    # Connect Nodes
    workflow.add_edge("retrieve", "generate")
    workflow.add_edge("generate", "validate")
    
    # Conditional edge from validation
    workflow.add_conditional_edges(
        "validate",
        validate_transition,
        {
            "generate": "generate",
            "execute": "execute"
        }
    )

    # Conditional edge from execution (for retries)
    workflow.add_conditional_edges(
        "execute",
        should_retry,
        {
            "retry": "generate",
            "execute": "explain",
            "fail": "explain" # Explain the failure finally
        }
    )

    workflow.add_edge("explain", END)

    return workflow.compile()
