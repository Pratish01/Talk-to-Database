import os
import shutil
from dotenv import load_dotenv
from src.rag.vectorstore import build_vectorstore
from src.config import VECTORSTORE_DIR, ROOT_DIR
from src.utils.llm_factory import get_embeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

def force_rebuild():
    if os.path.exists(VECTORSTORE_DIR):
        print(f"Deleting existing index at {VECTORSTORE_DIR}...")
        shutil.rmtree(VECTORSTORE_DIR)
    
    print("Rebuilding vector store...")
    schema_path = ROOT_DIR / "src" / "rag" / "schema_docs.json"
    build_vectorstore(str(schema_path))
    
    print("Verifying dimensions...")
    embeddings = get_embeddings()
    vectorstore = FAISS.load_local(
        VECTORSTORE_DIR, 
        embeddings, 
        allow_dangerous_deserialization=True
    )
    
    # Check index dimension
    print(f"Index dimension (self.d): {vectorstore.index.d}")
    
    # Check embedding dimension
    test_vec = embeddings.embed_query("test")
    print(f"Embedding dimension (d): {len(test_vec)}")
    
    if vectorstore.index.d == len(test_vec):
        print("SUCCESS: Dimensions match!")
    else:
        print("FAILURE: Dimensions mismatch!")

if __name__ == "__main__":
    force_rebuild()
