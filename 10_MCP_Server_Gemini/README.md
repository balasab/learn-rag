# Gemini MCP Server

This project implements a Model Context Protocol (MCP) server that exposes Google's Gemini models as tools and resources. It is designed to demonstrate how to integrate Large Language Models (LLMs) into the MCP ecosystem.

## Setup

1.  **Navigate to the directory:**
    ```bash
    cd 10_MCP_Server_Gemini
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up API Key:**
    - Get a Google Gemini API Key from [Google AI Studio](https://aistudio.google.com/).
    - Export it as an environment variable:
      ```bash
      export GOOGLE_API_KEY=your_api_key_here
      ```
      Or create a `.env` file in this directory with:
      ```
      GOOGLE_API_KEY=your_api_key_here
      ```

## Running the Server

### Using MCP Inspector (Recommended for testing)
If you have `npx` installed:
```bash
npx @modelcontextprotocol/inspector python server.py
```
This will open a web interface where you can list resources and run tools interactively.

### Running Directly
You can run the server directly, but it expects to communicate via stdio with an MCP client (like Claude Desktop or an IDE extension).
```bash
python server.py
```

## Tools & Resources

-   **Tool: `gemini_chat`**: Sends a prompt to Gemini and acts as a chatbot.
-   **Tool: `summarize_text`**: Takes a block of text and returns a concise summary.
-   **Resource: `gemini://models`**: Lists available Gemini models that support content generation.

## Interview Guide: Explaining this Code

### 1. What is MCP?
**Answer:** MCP (Model Context Protocol) is an open standard that enables AI assistants (clients) to connect to data and systems (servers). It standardizes how AI tools discover and interact with external resources.

### 2. How does this server work?
**Answer:**
-   **Server Initialization:** We use `FastMCP` from the `mcp` SDK to create a server instance.
-   **Decorator Pattern:** We use decorators like `@mcp.tool()` and `@mcp.resource()` to register Python functions as MCP capabilities.
-   **Transport:** The server runs over standard input/output (stdio), which is the default transport for local MCP integrations.
-   **Integration:** Inside the tools, we use the `google-generativeai` SDK to make calls to the Gemini API.

### 3. Key Components
-   **Resources:** Expose data (like a list of models) for the client to read.
    -   *Example:* `gemini://models` lets the client know what models it can ask for.
-   **Tools:** Expose executable functions (like chatting or summarizing) that the client can call.
    -   *Example:* `summarize_text` allows the LLM to offload a specific task to your defined logic (which in this case calls another LLM, but could be a database query).

### 4. Why use MCP here?
**Answer:**
-   **Standardization:** Instead of writing custom API wrappers for every different tool (Slack, Jira, Gemini), MCP provides a single protocol.
-   **Modularity:** This server can be plugged into *any* MCP-compliant client (Claude Desktop, Zed, etc.) without changing a single line of code.

### 5. Error Handling
**Answer:** We wrap external API calls in `try...except` blocks to ensure the server doesn't crash if the API is down or the key is invalid. We return error messages as strings so the model knows something went wrong.
