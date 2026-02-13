import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_groq import ChatGroq
from src.config import LLM_PROVIDER, OPENAI_API_KEY, GOOGLE_API_KEY, GROQ_API_KEY, MODEL_NAME

def get_llm(temperature=0):
    """Factory function to get the appropriate LLM based on provider."""
    if LLM_PROVIDER == "openai":
        return ChatOpenAI(
            openai_api_key=OPENAI_API_KEY,
            model_name=MODEL_NAME,
            temperature=temperature
        )
    elif LLM_PROVIDER == "google":
        return ChatGoogleGenerativeAI(
            google_api_key=GOOGLE_API_KEY,
            model=MODEL_NAME,
            temperature=temperature
        )
    elif LLM_PROVIDER == "groq":
        return ChatGroq(
            api_key=GROQ_API_KEY,
            model_name=MODEL_NAME,
            temperature=temperature
        )
    else:
        raise ValueError(f"Unsupported LLM provider: {LLM_PROVIDER}")

def get_embeddings():
    """Factory function to get the appropriate Embeddings based on provider."""
    # Prioritize Google if key is available, as it's often the current fallback for non-OpenAI setups
    if GOOGLE_API_KEY:
        return GoogleGenerativeAIEmbeddings(google_api_key=GOOGLE_API_KEY, model="models/gemini-embedding-001")
    elif LLM_PROVIDER == "openai" and OPENAI_API_KEY:
        return OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    else:
        # Final fallback/error
        if LLM_PROVIDER == "openai":
            raise ValueError("OpenAI API Key not found for embeddings.")
        print(f"Warning: No specific embeddings provider configured for {LLM_PROVIDER}, and no Google API key found. Attempting OpenAI fallback...")
        return OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
