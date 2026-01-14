# Mocking tools for the agent
def search_tool(query):
    print(f"  [Tool: Search] Searching for: '{query}'")
    if "weather" in query.lower():
        return "The weather in New York is 72F and sunny."
    if "rag" in query.lower():
        return "RAG combines retrieval and generation."
    return "No relevant info found."

def calculator_tool(expression):
    print(f"  [Tool: Calculator] Calculating: {expression}")
    try:
        return str(eval(expression))
    except:
        return "Error"

class Agent:
    def __init__(self):
        self.history = []
    
    def decide_action(self, query):
        # In a real agent, this is an LLM call: 
        # response = check_if_tools_needed(query)
        
        print(f"\n--- Agent thinking about: '{query}' ---")
        
        # Simple heuristic logic to simulate "Agentic" reasoning
        if "weather" in query.lower() or "rag" in query.lower():
            return "search", query
        elif any(op in query for op in ["+", "-", "*", "/"]):
            return "calc", query
        else:
            return "answer", query

    def run(self, query):
        action, parameter = self.decide_action(query)
        
        if action == "search":
            print("  [Thought] I need external information.")
            result = search_tool(parameter)
            print(f"  [Observation] Found: {result}")
            print(f"  [Final Answer] Based on search: {result}")
            
        elif action == "calc":
            print("  [Thought] This looks like a math problem.")
            result = calculator_tool(parameter)
            print(f"  [Final Answer] The result is {result}")
            
        else:
            print("  [Thought] I can answer this from my internal knowledge.")
            print(f"  [Final Answer] {query} is a general conversation topic.")

if __name__ == "__main__":
    agent = Agent()
    agent.run("What is the weather in New York?")
    agent.run("Calculate 25 * 4")
    agent.run("Hello, how are you?")
