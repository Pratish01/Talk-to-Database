from src.state import AgentState
from src.rag.vectorstore import get_retriever

def retrieval_node(state: AgentState) -> AgentState:
    """Retrieves relevant schema context from the vector store."""
    print("--- RETRIEVING SCHEMA CONTEXT ---")
    question = state["question"]
    retriever = get_retriever()
    
    docs = retriever.invoke(question)
    context = "\n\n".join([doc.page_content for doc in docs])
    
    return {
        **state,
        "schema_context": context
    }
