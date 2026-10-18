from typing import Literal, Optional,Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

class AgentState(TypedDict, total=False):
    messages: Annotated[list[BaseMessage],add_messages]
    route: Literal["search","answer","unknown"]
    