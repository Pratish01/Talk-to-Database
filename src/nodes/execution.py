import pandas as pd
from sqlalchemy import create_engine
from src.state import AgentState
from src.config import DATABASE_URL

def execution_node(state: AgentState) -> AgentState:
    """Executes the validated SQL query on the read-only database."""
    print("--- EXECUTING SQL QUERY ---")
    sql = state["sql_query"]
    
    try:
        engine = create_engine(DATABASE_URL)
        # Using pandas for easy formatting of results
        df = pd.read_sql_query(sql, engine)
        result = df.to_dict(orient="records")
        
        return {
            **state,
            "sql_result": result,
            "error": None
        }
    except Exception as e:
        print(f"Execution Error: {str(e)}")
        return {
            **state,
            "error": f"SQL Execution Error: {str(e)}",
            "retry_count": state["retry_count"] + 1
        }
