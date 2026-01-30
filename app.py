import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.messages import HumanMessage

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

    # Create a test query
    query = "What is 25 * 4 + 10?"
    print(f"📝 Sending query to AI: {query}")

    # Call llm.invoke() with the query
    response = chat.invoke([HumanMessage(content=query)])

    # Print the response content
    print("💬 AI Response:", response.content)

    print("🚀 Application has completed!")

if __name__ == "__main__":
    main()