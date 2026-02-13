# Talk to Database System (LangGraph + RAG)

A production-style system to query a SQL database using natural language.

## Architecture
- **RAG (FAISS)**: Stores and retrieves schema context and business rules.
- **LangGraph**: Orchestrates the multi-step workflow:
  - `retrieval`: Fetches relevant schema descriptions.
  - `generation`: Crafts SQL with safety guards.
  - `validation`: Ensures only SELECT queries and safety constraints.
  - `execution`: Runs SQL on a read-only database with retry logic.
  - `explanation`: Translates data into natural language.

## Prerequisites
- Python 3.9+
- An API Key (OpenAI, Google Gemini, or Groq)

## Setup
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file based on `.env.example`.
4. Set `LLM_PROVIDER` to `google` (for free Gemini API) or `openai`.
5. Add your corresponding API key (e.g., `GOOGLE_API_KEY` from [Google AI Studio](https://aistudio.google.com/)).

## Running the Project
Simply run the main script. It will automatically initialize the sample database and the vector store:
```bash
python -m src.main
```

## Example Queries
- "Who is the highest paid person and what is their role?"
- "What is the total budget for projects in the Engineering department?"
- "List all employees in the Sales department."
- "Show me the manager for the Marketing department."

## Safety
The system strictly enforces:
- `SELECT` queries only.
- `LIMIT 100` enforcement.
- Schema awareness via RAG to prevent hallucination.
- Retry mechanism for SQL execution errors.
