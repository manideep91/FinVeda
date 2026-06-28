import os
from dotenv import load_dotenv

load_dotenv()

def get_llm():
    """
    LLM factory method.
    
    Java analogy: This is a @Bean factory method in a @Configuration class.
    Swap LLM_PROVIDER in .env to change the LLM — zero code change needed.
    """
    provider = os.getenv("LLM_PROVIDER", "gemini")
    model = os.getenv("LLM_MODEL", "gemini-2.5-flash-lite")
    project = os.getenv("GOOGLE_CLOUD_PROJECT")

    if provider == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(
            model=model,
            vertexai=True,
            project=project
        )

    # Future providers drop in here cleanly:
    # if provider == "anthropic": ...
    # if provider == "openai": ...

    raise ValueError(f"Unknown LLM_PROVIDER: {provider}")