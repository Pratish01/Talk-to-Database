from typing import TypedDict, List, Optional, Any

class AgentState(TypedDict):
    question: str
    schema_context: str
    sql_query: str
    sql_result: Any
    explanation: str
    error: Optional[str]
    retry_count: int
    history: List[str]
