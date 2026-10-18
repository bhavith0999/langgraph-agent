"""node functions ofr the agent graph . each node reads state and returns an update"""

import os
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from src.agent.state import AgentState
from langchain_core.messages import HumanMessage, AIMessage,SystemMessage

#create llm once 
llm = ChatAnthropic(model="claude-haiku-4-5-20251001")

def router_node(state: AgentState) -> dict:
    """decided wheather a question neeeds websearch or a direct answer
    Returns:
        A dict updating 'route' to either 'search' or 'answer'."""
    prompt = ChatPromptTemplate.from_template(
        """You are a routing assistant. Classify this question into one of two categories:
        
- 'search': needs current/real-time information (news, prices, weather, recent events)
- 'answer': can be answered from general knowledge

Question: {question}

Reply with ONLY the single word: search or answer"""
    )
    chain = prompt | llm
    print(f"debug state: {state}")
    response = chain.invoke({"question": state["messages"][-1].content})#gets the latest message
    route = response.content.strip().lower() 
    # DEBUG — remove after fixing
    print(f"DEBUG raw route: '{route}'")
     # Safety check — default to 'answer' if unexpected response
    if route not in ("search", "answer"):
        route = "answer"

    return {"route": route}


def answer_node(state: AgentState) -> dict:
    #question =state["question"]
    messages_with_system = SystemMessage(content="You are a helpful research assistant. Give clear, concise answers based only on what you know. If you are unsure, say so.") 
    response = llm.invoke(messages_with_system)
    print(f"{response}")
    return {"messages":[AIMessage(content=response.content)]}

def search_node(state: AgentState) -> dict:
    """Placeholder for web search — we'll wire real search in the next step.

    Returns:
        A dict updating 'answer' with a placeholder message.
    """
    from tavily import TavilyClient
    import os
    question = state["messages"][-1].content  # ← add this
    client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    result = client.search(query=question, max_results=3) #search is a tavily feature just like ll.invoke 
    content = "\n\n".join(r["content"] for r in result["results"])
    

    # # Ask Claude to summarise the raw results into a clean answer
    # prompt = f"""Based on the following search results, answer this question clearly and concisely:

    # Question: {state["question"]}

    prompt = f"Based on these search results, answer clearly:\n\n{content}\n\nQuestion: {question}"
    response = llm.invoke(prompt)
    return {"messages": [AIMessage(content=response.content)]}

