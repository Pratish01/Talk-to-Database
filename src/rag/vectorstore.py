import json
import os
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from src.config import VECTORSTORE_DIR
from src.utils.llm_factory import get_embeddings

def build_vectorstore(schema_source):
    """Indexes schema documentation into a FAISS vector store.
    
    schema_source can be a path (str) or a list of dictionaries.
    """
    if isinstance(schema_source, str):
        if not os.path.exists(schema_source):
            print(f"Schema docs not found at {schema_source}")
            return
        with open(schema_source, "r") as f:
            schema_data = json.load(f)
    else:
        schema_data = schema_source

    documents = []
    for item in schema_data:
        # Create a rich text representation for retrieval
        content = f"Name: {item.get('name')}\nType: {item.get('type')}\nDescription: {item.get('description')}\n"
        if "columns" in item:
            cols = ", ".join([f"{c['name']} ({c['description']})" for c in item["columns"]])
            content += f"Columns: {cols}"
        
        doc = Document(
            page_content=content,
            metadata={"id": item["id"], "type": item["type"], "name": item.get("name", "")}
        )
        documents.append(doc)

    embeddings = get_embeddings()
    vectorstore = FAISS.from_documents(documents, embeddings)
    
    os.makedirs(VECTORSTORE_DIR, exist_ok=True)
    vectorstore.save_local(VECTORSTORE_DIR)
    print(f"Vector store saved to {VECTORSTORE_DIR}")

def get_retriever():
    """Returns a retriever for the schema documentation."""
    embeddings = get_embeddings()
    vectorstore = FAISS.load_local(
        VECTORSTORE_DIR, 
        embeddings, 
        allow_dangerous_deserialization=True
    )
    return vectorstore.as_retriever(search_kwargs={"k": 5})

if __name__ == "__main__":
    # For testing/initialization
    from src.config import ROOT_DIR
    build_vectorstore(ROOT_DIR / "src" / "rag" / "schema_docs.json")
