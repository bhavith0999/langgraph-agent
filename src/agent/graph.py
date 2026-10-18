from langgraph.graph import StateGraph, START, END
from src.agent.state import AgentState
from src.agent.nodes import router_node, answer_node, search_node
from langgraph.checkpoint.memory import MemorySaver

def route_decision(state: AgentState) -> str:
    """Reads the router's decision from state and returns the next node name."""
    return state["route"]

def build_graph():
    """Assemble the nodes and edges into a runnable graph.

    Returns:
        A compiled LangGraph app ready to invoke.
    """
    builder = StateGraph(AgentState) #state graph is like blueprint holder for our agent
     # Add all three nodes
    builder.add_node("router", router_node)
    builder.add_node("answerer", answer_node)
    builder.add_node("searcher", search_node)
    builder.add_edge(START, "router")
    builder.add_conditional_edges(
        "router",           # from this node
        route_decision,     # call this function to decide
        {
            "answer": "answerer",   # if returns "answer" -> go to answerer
            "search": "searcher",   # if returns "search" -> go to searcher
        }
    )

    builder.add_edge("answerer", END)
    builder.add_edge("searcher", END)
    memory = MemorySaver()
    return builder.compile(checkpointer=memory)