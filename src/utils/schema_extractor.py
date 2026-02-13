from sqlalchemy import create_engine, inspect
from typing import List, Dict, Any

def extract_schema(db_url: str) -> List[Dict[str, Any]]:
    """Automatically extracts schema information from a database using SQLAlchemy."""
    print(f"Extracting schema from connection...")
    
    engine = create_engine(db_url)
    inspector = inspect(engine)
    
    tables = inspector.get_table_names()
    schema_docs = []
    
    for table_name in tables:
        columns_info = inspector.get_columns(table_name)
        
        columns = []
        for col in columns_info:
            # col structure: {'name': str, 'type': TypeEngine, 'nullable': bool, 'default': str, 'autoincrement': bool, 'comment': str}
            columns.append({
                "name": col['name'],
                "description": f"Column of type {str(col['type'])}"
            })
            
        schema_docs.append({
            "id": f"table_{table_name}",
            "type": "table_schema",
            "name": table_name,
            "description": f"Table containing information about {table_name}.",
            "columns": columns
        })
        
    return schema_docs

if __name__ == "__main__":
    import os
    import sys
    # Add project root to sys.path
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    from src.config import DATABASE_PATH
    
    schema = extract_schema(str(DATABASE_PATH))
    import json
    print(json.dumps(schema, indent=2))
