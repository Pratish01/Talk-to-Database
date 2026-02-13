import sys
import os
from pathlib import Path

# Add project root to sys.path to allow 'src' imports
ROOT_DIR = Path(__file__).parent.parent
sys.path.append(str(ROOT_DIR))

from src.graph import define_graph
from src.utils.db_setup import create_sample_db
from src.rag.vectorstore import build_vectorstore
from src.config import DATABASE_PATH, VECTORSTORE_DIR, IS_EXTERNAL_DB
from src.utils.schema_extractor import extract_schema

def initialize_system():
    """Initializes the database and vector store."""
    import os
    
    # Only create sample DB if no external DB is provided
    if not IS_EXTERNAL_DB and not os.path.exists(DATABASE_PATH):
        create_sample_db()
    
    # Index the database schema
    # Forced for external DBs to ensure indexing is correct
    if IS_EXTERNAL_DB or not os.path.exists(VECTORSTORE_DIR):
        print(f"Indexing schema for {'external' if IS_EXTERNAL_DB else 'sample'} database...")
        if IS_EXTERNAL_DB:
            schema_data = extract_schema(str(DATABASE_PATH))
            build_vectorstore(schema_data)
        else:
            schema_path = ROOT_DIR / "src" / "rag" / "schema_docs.json"
            build_vectorstore(str(schema_path))

def main():
    print("=== TALK TO DATABASE SYSTEM ===")
    initialize_system()
    
    app = define_graph()
    
    while True:
        try:
            print("\nEnter your question in natural language (or type 'exit' to quit):")
            user_input = input("> ").strip()
            
            if user_input.lower() in ["exit", "quit"]:
                break
                
            if not user_input:
                continue
                
            inputs = {
                "question": user_input,
                "retry_count": 0,
                "history": []
            }
            
            # Stream the graph execution for transparency
            for output in app.stream(inputs):
                for node_name, state_update in output.items():
                    # We can print debugging info here if needed
                    # print(f"--- Node '{node_name}' finished ---")
                    pass
            
            # Final result is in the last state update
            # Since stream yields updates, we need the final state
            final_state = app.invoke(inputs)
            
            print(f"\n[AI RESPONSE]: {final_state['explanation']}")
            print("-" * 30)
            print(f"[DEBUG SQL]: {final_state.get('sql_query')}")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception:
            import traceback
            print("\n--- CRITICAL SYSTEM ERROR ---")
            traceback.print_exc()
            print("------------------------------")

if __name__ == "__main__":
    main()
