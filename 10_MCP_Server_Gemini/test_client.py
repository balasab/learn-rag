import asyncio
import os
from dotenv import load_dotenv

# Since we are testing internal logic without a full MCP client, 
# we can import the functions directly to test logic if we restructure, 
# OR we can use the mcp client libraries to connect to the running server.
# For simplicity in this interview prep, we will verify the Gemini logic directly.

from server import gemini_chat, summarize_text, list_models

async def main():
    load_dotenv()
    if not os.getenv("GOOGLE_API_KEY"):
        print("Error: GOOGLE_API_KEY not set. Please set it to run the test.")
        return

    print("--- Testing Gemini Chat ---")
    response = await gemini_chat("Hello, tell me a one-sentence joke.")
    print(f"Response: {response}\n")

    print("--- Testing Summarization ---")
    text = """
    The generic name for the technique of retrieval-augmented generation (RAG) 
    is a pattern in which an application retrieves information 
    relevant to a user's query and provides it to the language model 
    as part of the prompt. This allows the model to answer questions 
    about private or specific data it wasn't trained on.
    """
    summary = await summarize_text(text)
    print(f"Summary: {summary}\n")

    print("--- Testing Resource Listing ---")
    # Resources are not async in FastMCP definition unless specified, 
    # but accessing them via client would be. Here we call the function directly.
    models = list_models()
    print(f"Models:\n{models}")

if __name__ == "__main__":
    asyncio.run(main())
