import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from src.config import VECTORSTORE_DIR
from src.utils.llm_factory import get_embeddings

load_dotenv()

def test_load():
    try:
        print(f"Attempting to load index from {VECTORSTORE_DIR}...")
        embeddings = get_embeddings()
        vectorstore = FAISS.load_local(
            VECTORSTORE_DIR, 
            embeddings, 
            allow_dangerous_deserialization=True
        )
        print("Index loaded successfully!")
        
        # Try a quick retrieval
        print("Testing retrieval...")
        docs = vectorstore.similarity_search("test")
        print(f"Retrieved {len(docs)} documents.")
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_load()
