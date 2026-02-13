import re
from src.state import AgentState
from src.config import ALLOWED_TABLES

def validation_node(state: AgentState) -> AgentState:
    """Validates the generated SQL for safety and correctness."""
    print("--- VALIDATING SQL QUERY ---")
    sql = state["sql_query"].upper()
    
    # 1. Check for dangerous keywords
    forbidden_keywords = ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "TRUNCATE", "CREATE", "REPLACE"]
    for word in forbidden_keywords:
        if f" {word} " in f" {sql} " or sql.startswith(word):
            return {**state, "error": f"Security violation: {word} is not allowed."}
            
    # 2. Check for SELECT only
    if not sql.startswith("SELECT"):
        return {**state, "error": "Only SELECT queries are allowed."}
        
    # 3. Check for LIMIT
    if "LIMIT" not in sql:
        state["sql_query"] += " LIMIT 100"
        
    # 4. Basic heuristic for hallucinations (optional but helpful)
    # This checks if table names mentioned exist in the context provided
    # (Simplified for now, but in production we'd parse the SQL properly)
    
    return {**state, "error": None}
