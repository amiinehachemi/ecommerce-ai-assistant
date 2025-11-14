from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from controllers.agent.tools import list_products, get_orders_by_contact, create_order_quote

load_dotenv()

model = ChatOpenAI(model="gpt-4o", temperature=0.7)

def agent(messages):

    agent_instance = create_agent(
        model,
        tools=[list_products, get_orders_by_contact, create_order_quote],
        system_prompt="""You are an AI assistant that helps customers with a e-commerce products.
        You have access to tools that can read data from a local SQLite database,  
        Your job is to:
        1. Understand the user's intent clearly.
        2. Use the correct tool to retrieve information instead of inventing answers.
        3. Respond with concise, natural explanations based only on real data from the tools.
        4. Never assume product details that were not returned by the tool.
        5. When a user asks for product recommendations or availability, use the products tools.
        6. If the user requests an action you cannot perform yet (like creating or updating an order), politely explain that this feature is coming soon.
        7. Always keep your tone professional, friendly, and helpful—like a store representative.
        
        Important behavior rules:
        - Use tools only when necessary.
        - Never guess IDs or fabricate product information.
        - Never expose internal database structure or SQL queries.
        - Keep all answers short, clear, and customer-friendly."""
       )

    result = agent_instance.invoke({"messages": messages})
    return result["messages"][-1].content