import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.messages import HumanMessage
from langchain.agents import create_agent
from langchain_core.tools import Tool
from datetime import datetime

def calculator(expression: str) -> str:
    """
    Evaluates a mathematical expression provided as a string.

    Args:
        expression (str): The mathematical expression to evaluate.

    Returns:
        str: The result of the evaluation as a string.
    """
    try:
        # Evaluate the expression using eval (for demo purposes, use with caution)
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error: {e}"

def get_current_time(input: str) -> str:
    """
    Returns the current date and time.

    Args:
        input (str): A string input parameter (required by the Tool interface).

    Returns:
        str: The current date and time in the format 'YYYY-MM-DD HH:MM:SS'.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def reverse_string(input: str) -> str:
    """
    Reverses a string.

    Args:
        input (str): The string to reverse.

    Returns:
        str: The reversed string.
    """
    return input[::-1]

def main():
    # Load environment variables from .env file
    load_dotenv()

    # Check if GITHUB_TOKEN exists in environment variables
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        print("❌ Error: GITHUB_TOKEN not found in environment variables.")
        print("💡 Please create a .env file and add GITHUB_TOKEN=<your_token>.")
        print("   Example:")
        print("   GITHUB_TOKEN=ghp_yourPersonalAccessToken")
        return  # Exit early if no token is found

    print("✅ GITHUB_TOKEN loaded successfully!")

    # Create a ChatOpenAI instance
    chat = ChatOpenAI(
        model="openai/gpt-4o",
        temperature=0,  # Deterministic responses
        base_url="https://models.github.ai/inference",
        api_key=github_token
    )

    print("🤖 ChatOpenAI instance created successfully!")

    # Add all three tools to the tools list
    tools = [
        Tool(
            name="Calculator",
            func=calculator,
            description="Use this tool to evaluate mathematical expressions. Provide the expression as a string, and it will return the result."
        ),
        Tool(
            name="get_current_time",
            func=get_current_time,
            description="Use this tool to get the current date and time in the format 'YYYY-MM-DD HH:MM:SS'."
        ),
        Tool(
            name="reverse_string",
            func=reverse_string,
            description="Reverses a string. Input should be a single string."
        )
    ]

    print("🛠️ Tools initialized successfully!")

    # Ensure agent_executor is defined even if tools are empty
    if tools:
        agent_executor = create_agent(
            chat,  # Pass the LLM as a positional argument
            tools,
            debug=False,  # Disable verbose output
            system_prompt="You are a professional and helpful AI assistant. Provide succinct, accurate responses."
        )
        print("🤖 Agent created successfully!")
    else:
        print("❌ No tools available. Agent cannot be created.")
        return

    # Replace the single query with a list of test queries
    test_queries = [
        "What time is it right now?",
        "What is 25 * 4 + 10?",
        "Reverse the string 'Hello World'"
    ]

    print("Running example queries:\n")

    # Iterate through each query
    for query in test_queries:
        print(f"📝 Query: {query}")
        print("─" * 50)
        try:
            # Call agent_executor.invoke() for each query
            result = agent_executor.invoke({"input": query, "messages": [HumanMessage(content=query)]})

            # Extract the output from the result object
            if isinstance(result, dict) and 'messages' in result and result['messages']:
                final_message = result['messages'][-1]  # Get the last message
                if hasattr(final_message, 'content'):
                    print(f"✅ Result: {final_message.content}\n")
                else:
                    print("❌ Error: Unable to extract content from the final message.\n")
            else:
                print("❌ Error: Unexpected result format.\n")
        except Exception as e:
            print(f"❌ Error: {str(e)}\n")

    print("🎉 Agent demo complete!\n")

if __name__ == "__main__":
    main()