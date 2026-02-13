import os
import asyncio
import google.generativeai as genai
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable not found")

genai.configure(api_key=API_KEY)

# Initialize FastMCP server
mcp = FastMCP("Gemini MCP Server")

@mcp.tool()
async def gemini_chat(query: str, model_name: str = "gemini-1.5-flash") -> str:
    """
    Chat with Gemini.
    
    Args:
        query: The prompt or question to ask Gemini.
        model_name: The model to use (default: gemini-1.5-flash).
    """
    try:
        model = genai.GenerativeModel(model_name)
        response = await model.generate_content_async(query)
        return response.text
    except Exception as e:
        return f"Error communicating with Gemini: {str(e)}"

@mcp.tool()
async def summarize_text(text: str) -> str:
    """
    Summarize a given text using Gemini.
    
    Args:
        text: The text content to summarize.
    """
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"Please summarize the following text concisely:\n\n{text}"
        response = await model.generate_content_async(prompt)
        return response.text
    except Exception as e:
        return f"Error summarizing text: {str(e)}"

@mcp.resource("gemini://models")
def list_models() -> str:
    """
    List available Gemini models.
    """
    try:
        models = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                models.append(m.name)
        return "\n".join(models)
    except Exception as e:
        return f"Error listing models: {str(e)}"

if __name__ == "__main__":
    # Standard stdio server start
    mcp.run()
