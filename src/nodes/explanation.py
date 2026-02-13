from langchain_core.prompts import ChatPromptTemplate
from src.state import AgentState
from src.utils.llm_factory import get_llm

def explanation_node(state: AgentState) -> AgentState:
    """Explains the SQL results in natural language."""
    print("--- EXPLAINING RESULTS ---")
    question = state["question"]
    sql = state["sql_query"]
    result = state.get("sql_result")
    error = state.get("error")
    
    prompt_text = """You are a helpful assistant that explains SQL query results to users in simple natural language.
    
    USER QUESTION: {question}
    SQL QUERY EXECUTED: {sql}
    DATA RETRIEVED: {result}
    ERROR: {error}
    
    If an error occurred, explain what went wrong in simple terms.
    If the data is empty and no error occurred, explain that no records were found.
    If the data exists, summarize it clearly to answer the user's specific question.
    Keep your answer concise and friendly.
    
    EXPLANATION:
    """
    
    prompt = ChatPromptTemplate.from_template(prompt_text)
    llm = get_llm(temperature=0.7)
    
    chain = prompt | llm
    response = chain.invoke({
        "question": question,
        "sql": sql,
        "result": str(result),
        "error": str(error)
    })
    
    return {
        **state,
        "explanation": response.content.strip()
    }
