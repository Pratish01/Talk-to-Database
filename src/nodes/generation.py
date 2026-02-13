from langchain_core.prompts import ChatPromptTemplate
from src.state import AgentState
from src.utils.llm_factory import get_llm
from src.config import DATABASE_URL

def generation_node(state: AgentState) -> AgentState:
    """Generates a SQL query based on the question and schema context."""
    print("--- GENERATING SQL QUERY ---")
    question = state["question"]
    context = state["schema_context"]
    error = state.get("error")
    
    dialect = "MySQL" if DATABASE_URL.startswith("mysql") else "SQLite"
    
    error_context_text = ""
    if error:
        error_context_text = f"PREVIOUS ERROR: {error}\nPlease fix the query based on this error."
        
    prompt_text = f"""You are a master SQL developer. Your task is to generate a SQL query to answer the following user question.
    
    CRITICAL CONSTRAINTS:
    - Use ONLY SELECT queries.
    - NEVER use INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE.
    - DO NOT hallucinate tables or columns.
    - ALWAYS apply a LIMIT 100 if no other limit is specified.
    - Use standard {dialect} syntax.
    
    RELEVANT SCHEMA CONTEXT:
    {{context}}
    
    USER QUESTION:
    {{question}}
    
    {{error_context}}
    
    YOUR SQL QUERY (output only the raw SQL, no markdown formatting):
    """
        
    prompt = ChatPromptTemplate.from_template(prompt_text)
    llm = get_llm(temperature=0)
    
    chain = prompt | llm
    response = chain.invoke({"question": question, "context": context, "error_context": error_context_text})
    
    sql_query = response.content.strip()
    # Basic cleaning in case LLM adds markdown
    if sql_query.startswith("```sql"):
        sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
    elif sql_query.startswith("```"):
        sql_query = sql_query.replace("```", "").strip()
        
    return {
        **state,
        "sql_query": sql_query,
        "error": None # Reset error for validation
    }
